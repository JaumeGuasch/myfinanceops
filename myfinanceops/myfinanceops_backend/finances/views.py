from django.views.generic import ListView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from finances.models import User, Operation
from finances.serializers import UserSerializer, StockOperationSerializer, \
    FuturesOperationSerializer, FuturesOptionsOperationSerializer
import jwt, datetime
from django.http import JsonResponse
from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation
import json


# Create your views here.

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': str(user.id),
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=180),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        print(f"Token: {token}")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(f"Payload: {payload}")
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]  # Allow access without authentication

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class CreateOperationView(APIView):
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
    def get(self, request):
        # Initialize an empty list to hold all operations
        all_operations = []

        # A mapping of subclasses to their serializers
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
        return Response(all_operations)
