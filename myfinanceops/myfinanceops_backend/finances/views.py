import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation
from finances.serializers import StockOperationSerializer, \
    FuturesOperationSerializer, FuturesOptionsOperationSerializer
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


class CreateOperationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        operation_type = data.get('type')
        common_fields = {key: data[key] for key in data if key not in ['type', 'specific_fields']}

        if operation_type == 'stock':
            operation = StockOperation(**common_fields, **data['specific_fields'])
        elif operation_type == 'futures':
            operation = FuturesOperation(**common_fields, **data['specific_fields'])
        elif operation_type == 'futures_options':
            operation = FuturesOptionsOperation(**common_fields, **data['specific_fields'])
        else:
            return JsonResponse({'error': 'Invalid operation type'}, status=400)

        operation.save()
        return JsonResponse({'message': 'Operation created successfully'}, status=201)


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
