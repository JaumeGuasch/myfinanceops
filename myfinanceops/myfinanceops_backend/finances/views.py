import json

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation, OperationChain, \
    Market, Operation, Commissions, OperationCommission
from finances.serializers import StockOperationSerializer, \
    FuturesOperationSerializer, FuturesOptionsOperationSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@api_view(['POST'])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(get_user_model(), email=email)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def signup(request):
    user = get_user_model()  # Get the custom user model
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = user.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"message": "Token is valid for {}".format(request.user.email)})


@api_view(['POST'])
def logout(request):
    try:
        # Retrieve the user's token and delete it
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        # If something goes wrong, return an error response
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({'message': 'Welcome to the finance operations API!'})


class OperationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        all_operations = []
        subclass_serializer_mapping = {
            StockOperation: StockOperationSerializer,
            FuturesOperation: FuturesOperationSerializer,
            FuturesOptionsOperation: FuturesOptionsOperationSerializer,
        }

        for subclass, serializer_class in subclass_serializer_mapping.items():
            subclass_instances = subclass.objects.all()
            serializer = serializer_class(subclass_instances, many=True)
            all_operations.extend(serializer.data)
        return Response(all_operations)


class CreateOperationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        operation_type = data.get('type')
        operation_chain_number = data.get('operation_chain', None)
        common_fields = {key: data[key] for key in data if key not in ['type', 'specific_fields', 'operation_chain']}
        specific_fields = data.get('specific_fields', {})

        if operation_chain_number:
            operation_chain = OperationChain.objects.get(chain_number=operation_chain_number)
            if operation_type == 'stockoperation':
                existing_operations = StockOperation.objects.filter(operation_chain=operation_chain)
            elif operation_type == 'futuresoperation':
                existing_operations = FuturesOperation.objects.filter(operation_chain=operation_chain)
            elif operation_type == 'futuresoptionsoperation':
                existing_operations = FuturesOptionsOperation.objects.filter(operation_chain=operation_chain)
            else:
                return JsonResponse({'error': 'Invalid operation type'}, status=400)

            if existing_operations.exists():
                existing_type = existing_operations.first()._meta.model_name
                if existing_type != operation_type:
                    return JsonResponse({'error': 'Operation type mismatch in the chain'}, status=400)
            common_fields['operation_chain'] = operation_chain
        else:
            operation_chain = OperationChain.objects.create()
            common_fields['operation_chain'] = operation_chain

        market_name = common_fields.pop('market', None)
        if market_name:
            market = Market.objects.get(name=market_name)
            common_fields['market'] = market

        common_fields['created_by'] = request.user
        common_fields['modified_by'] = request.user

        # Create operation based on type
        if operation_type == 'stockoperation':
            operation = StockOperation(**common_fields, **specific_fields)
        elif operation_type == 'futuresoperation':
            operation = FuturesOperation(**common_fields, **specific_fields)
        elif operation_type == 'futuresoptionsoperation':
            operation = FuturesOptionsOperation(**common_fields, **specific_fields)
        else:
            return JsonResponse({'error': 'Invalid operation type'}, status=400)

        operation.save()
        return JsonResponse({
            'message': 'Operation created successfully',
            'operation_chain': operation_chain.chain_number
        }, status=201)


class UpdateOperationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            operation_id = data.get('id')
            if not operation_id:
                return JsonResponse({'error': 'Operation ID is required'}, status=400)

            # Retrieve the StockOperation instance
            operation = StockOperation.objects.get(id=operation_id)

            # Update fields
            operation.date = data.get('date', operation.date)
            operation.trader = data.get('trader', operation.trader)
            operation.transaction_type = data.get('transaction_type', operation.transaction_type)
            operation.stock_code = data.get('stock_code', operation.stock_code)
            operation.shares_amount = data.get('shares_amount', operation.shares_amount)
            operation.price_per_share = data.get('price_per_share', operation.price_per_share)
            operation.description = data.get('description', operation.description)

            # Convert operation_chain to OperationChain instance
            operation_chain_id = data.get('operation_chain')
            if operation_chain_id:
                operation_chain = OperationChain.objects.get(id=operation_chain_id)
                operation.operation_chain = operation_chain

            # Convert market to Market instance
            market_id = data.get('market')
            if market_id:
                market = Market.objects.get(id=market_id)
                operation.market = market

            # Save the updated operation
            operation.save()

            return JsonResponse({'message': 'Operation updated successfully'}, status=200)

        except StockOperation.DoesNotExist:
            return JsonResponse({'error': 'Operation not found'}, status=404)
        except OperationChain.DoesNotExist:
            return JsonResponse({'error': 'Operation chain not found'}, status=404)
        except Market.DoesNotExist:
            return JsonResponse({'error': 'Market not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class OperationTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Define a dictionary mapping model names to labels
        model_labels = {
            'stockoperation': 'Stocks operation',
            'futuresoperation': 'Futures operation',
            'futuresoptionsoperation': 'Options operation'
        }

        # Get all models that are subclasses of Operation
        operation_models = [model for model in apps.get_models() if
                            issubclass(model, Operation) and model is not Operation]

        # Extract the names and labels of these models
        operation_types = [{'type': model._meta.model_name,
                            'label': model_labels.get(model._meta.model_name, model._meta.verbose_name)} for model in
                           operation_models]

        return JsonResponse({'operation_types': operation_types})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_http_methods(["DELETE"])
def delete_operation(request):
    try:
        data = json.loads(request.body)
        operation_id = data.get('id')
        if not operation_id:
            return JsonResponse({'error': 'Operation ID is required'}, status=400)

        # Retrieve the StockOperation instance
        operation = StockOperation.objects.get(id=operation_id)
        operation.delete()

        return JsonResponse({'message': 'Operation deleted successfully'}, status=200)

    except StockOperation.DoesNotExist:
        return JsonResponse({'error': 'Operation not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_operation_fields(request):
    operation_type = request.GET.get('type')
    allowed_types = ['stockoperation', 'futuresoperation', 'futuresoptionsoperation']

    if not operation_type or operation_type not in allowed_types:
        return JsonResponse({'error': 'Valid operation type is required'}, status=400)

    common_fields = [
        {'name': 'date', 'label': 'Date', 'type': 'date'},
        {'name': 'trader', 'label': 'Trader', 'type': 'text'},
        {'name': 'market', 'label': 'Market', 'type': 'text'},
        {'name': 'transaction_type', 'label': 'Transaction Type', 'type': 'select', 'options': ['Buy', 'Sell']},
    ]

    if operation_type == 'stockoperation':
        specific_fields = [
            {'name': 'stock_code', 'label': 'Stock Code', 'type': 'text'},
            {'name': 'shares_amount', 'label': 'Shares Amount', 'type': 'number'},
            {'name': 'price_per_share', 'label': 'Price per Share', 'type': 'number'},
        ]
    elif operation_type == 'futuresoperation':
        specific_fields = [
            {'name': 'contract', 'label': 'Contract', 'type': 'text'},
            {'name': 'price_per_contract', 'label': 'Price per Contract', 'type': 'number'},
        ]
    elif operation_type == 'futuresoptionsoperation':
        specific_fields = [
            {'name': 'strike_price', 'label': 'Strike Price', 'type': 'number'},
            {'name': 'premium', 'label': 'Premium', 'type': 'number'},
            {'name': 'price_per_contract', 'label': 'Price per Contract', 'type': 'number'},
        ]
    else:
        specific_fields = []

    # Combine common fields with specific fields
    fields = common_fields + specific_fields

    return JsonResponse(fields, safe=False)


def get_all_operation_chain(request):
    operation_type = request.GET.get('type')
    if operation_type:
        if operation_type == 'stockoperation':
            operation_chains = OperationChain.objects.filter(
                stock_operation_chain__isnull=False
            ).distinct().values('id', 'chain_number')
        elif operation_type == 'futuresoperation':
            operation_chains = OperationChain.objects.filter(
                futures_operation_chain__isnull=False
            ).distinct().values('id', 'chain_number')
        elif operation_type == 'futuresoptionsoperation':
            operation_chains = OperationChain.objects.filter(
                futures_options_operation_chain__isnull=False
            ).distinct().values('id', 'chain_number')
        else:
            return JsonResponse({'error': 'Invalid operation type'}, status=400)
    else:
        operation_chains = OperationChain.objects.all().values('id', 'chain_number')

    return JsonResponse(list(operation_chains), safe=False)


def get_markets(request):
    markets = Market.objects.all().values()
    return JsonResponse(list(markets), safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_market(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        mic = data.get('mic')
        trading_days = data.get('trading_days', [])
        currency = data.get('currency')
        notes = data.get('notes', '')

        if not name or not mic or not currency:
            return JsonResponse({'error': 'Name, MIC, and currency are required'}, status=400)

        market = Market.objects.create(
            name=name,
            mic=mic,
            trading_days=trading_days,
            currency=currency,
            notes=notes
        )
        return JsonResponse({
            'message': 'Market created successfully',
            'market': {
                'id': market.id,
                'name': market.name,
                'mic': market.mic,
                'trading_days': market.trading_days,
                'currency': market.currency,
                'notes': market.notes
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_market(request):
    try:
        data = json.loads(request.body)
        market_ids = data.get('ids', [])
        if not market_ids:
            return JsonResponse({'error': 'Market IDs are required'}, status=400)

        Market.objects.filter(id__in=market_ids).delete()
        return JsonResponse({'message': 'Markets deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_commissions(request):
    commissions = Commissions.objects.all().values('id', 'name', 'created_by', 'modified_by')
    return JsonResponse(list(commissions), safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_commission(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        commission = Commissions.objects.create(
            name=name,
            created_by=request.user,
            modified_by=request.user
        )
        return JsonResponse({
            'message': 'Commission created successfully',
            'commission': {
                'id': commission.id,
                'name': commission.name,
                'created_by': commission.created_by.id,
                'modified_by': commission.modified_by.id
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_commission(request):
    try:
        data = json.loads(request.body)
        commission_ids = data.get('ids', [])
        if not commission_ids:
            return JsonResponse({'error': 'Commission IDs are required'}, status=400)

        Commissions.objects.filter(id__in=commission_ids).delete()
        return JsonResponse({'message': 'Commissions deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(["POST"])
def add_commission(request):
    try:
        data = json.loads(request.body)
        operation_id = data.get('operation_id')
        commission_id = data.get('commission_id')
        amount = data.get('amount')
        currency = data.get('currency')
        operation = Operation.objects.get(id=operation_id)
        commission = Commissions.objects.get(id=commission_id)

        OperationCommission.objects.create(
            content_type=ContentType.objects.get_for_model(operation),
            object_id=operation.id,
            commission=commission,
            amount=amount,
            currency=currency
        )

        return JsonResponse({'message': 'Commission added successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(["DELETE"])
def delete_commission(request):
    try:
        data = json.loads(request.body)
        operation_id = data.get('operation_id')
        commission_id = data.get('commission_id')
        operation = Operation.objects.get(id=operation_id)
        commission = Commissions.objects.get(id=commission_id)

        OperationCommission.objects.filter(
            content_type=ContentType.objects.get_for_model(operation),
            object_id=operation.id,
            commission=commission
        ).delete()

        return JsonResponse({'message': 'Commission deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
