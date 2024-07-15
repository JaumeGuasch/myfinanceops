import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from finances.decorators import jwt_required
from finances.models import User
from finances.serializers import UserSerializer, StockOperationSerializer, \
    FuturesOperationSerializer, FuturesOptionsOperationSerializer
import jwt
from django.http import JsonResponse
from finances.models import StockOperation, FuturesOperation, FuturesOptionsOperation
from django.views import View
import logging
import json


# Create your views here.

class JWTAuthenticationMixin(View):
    @method_decorator(jwt_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        logger = logging.getLogger(__name__)
        email = request.data['email']
        password = request.data['password']

        logger.debug(f"Login attempt for username: {email}")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': str(user.id),
            'exp': datetime.now() + timedelta(minutes=180),
            'iat': datetime.now(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, secure=False, samesite='Lax')
        response.data = {
            'message': 'Login successful',
            'jwt': token,
            'email': email
        }
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class CreateOperationView(JWTAuthenticationMixin, APIView):
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


class OperationsView(JWTAuthenticationMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
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
