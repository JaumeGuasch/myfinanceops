from functools import wraps
import jwt
from django.conf import settings
from django.dispatch.dispatcher import logging
from django.http import JsonResponse


logger = logging.getLogger(__name__)

def jwt_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        logger.debug(f"Cookies received: {request.COOKIES}")

        token = request.COOKIES.get('jwt')
        if not token:
            logger.warning("No JWT token found in cookies")
            return JsonResponse({'error': 'Unauthenticated'}, status=401)
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.error("JWT token expired")
            return JsonResponse({'error': 'Unauthenticated'}, status=401)
        except jwt.DecodeError:
            logger.error("Error decoding JWT token")
            return JsonResponse({'error': 'Unauthenticated'}, status=401)
        except Exception as e:
            logger.exception(f"Unexpected error in JWT authentication: {e}")
            return JsonResponse({'error': 'Unauthenticated'}, status=401)
        return f(request, *args, **kwargs)

    return wrap
