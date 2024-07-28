import json
from django.apps import apps
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation, OperationChain, Operation, Market
from finances.serializers import StockOperationSerializer, \
    FuturesOperationSerializer, FuturesOptionsOperationSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

@api_view(['POST'])
def login(request):
    try:
        print(request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(get_user_model(), email=email)
        print(user.email)
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.data)
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
        print(request.user)

        subclass_serializer_mapping = {
            StockOperation: StockOperationSerializer,
            FuturesOperation: FuturesOperationSerializer,
            FuturesOptionsOperation: FuturesOptionsOperationSerializer,
        }

        # Iterate over each subclass and its serializer
        for subclass, serializer_class in subclass_serializer_mapping.items():
            # Query all instances of the subclass
            subclass_instances = subclass.objects.all()
            # Serialize the data
            serializer = serializer_class(subclass_instances, many=True)
            # Add the serialized data to the list of all operations
            all_operations.extend(serializer.data)

        # Return the combined data
        print(all_operations)
        return Response(all_operations)


class CreateOperationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        operation_type = data.get('type')
        operation_chain_number = data.get('operation_chain', None)
        common_fields = {key: data[key] for key in data if key not in ['type', 'specific_fields', 'operation_chain']}
        specific_fields = data.get('specific_fields', {})

        # Handle operation_chain
        if operation_chain_number:
            operation_chain = OperationChain.objects.get(chain_number=operation_chain_number)
            common_fields['operation_chain'] = operation_chain
        else:
            # Create a new chain
            operation_chain = OperationChain.objects.create()
            common_fields['operation_chain'] = operation_chain

        # Fetch the Market instance
        market_name = common_fields.pop('market', None)
        if market_name:
            market = Market.objects.get(name=market_name)
            common_fields['market'] = market

        # Set the created_by and modified_by fields to the current user
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


def get_operation_fields(request):
    operation_type = request.GET.get('type')
    allowed_types = ['stockoperation', 'futuresoperation', 'futuresoptionsoperation']

    if not operation_type or operation_type not in allowed_types:
        return JsonResponse({'error': 'Valid operation type is required'}, status=400)

    # Common fields for all operations
    common_fields = [
        {'name': 'date', 'label': 'Date', 'type': 'date'},
        {'name': 'trader', 'label': 'Trader', 'type': 'text'},
        {'name': 'market', 'label': 'Market', 'type': 'text'},
        {'name': 'transaction_type', 'label': 'Transaction Type', 'type': 'select', 'options': ['buy', 'sell']},
    ]

    # Specific fields based on operation type
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
    operation_chains = OperationChain.objects.all().values('id', 'chain_number')
    return JsonResponse(list(operation_chains), safe=False)
