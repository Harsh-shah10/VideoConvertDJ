from django.http import JsonResponse
from django.conf import settings
from jwt import decode, InvalidTokenError
from .models import *
from datetime import datetime

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is excluded from token check
        EXCLUDE_FROM_TOKEN_CHECK = ['/account/signup/','/account/login/']
        if request.path in EXCLUDE_FROM_TOKEN_CHECK:
            return self.get_response(request)

        auth_header = request.headers.get('token')
        if not auth_header:
            return JsonResponse({'status':'fail', 'message': 'token header missing', 'status_code':401}, status=401)

        try:
            try:
                token_check = Token.objects.get(unique_token = auth_header)
            except:
                return JsonResponse({'status':'fail', 'message': 'Invalid token', 'status_code':401}, status=401)
            from django.utils import timezone
            if token_check.expiry < timezone.now():
                return JsonResponse({'status':'fail', 'message': 'Token Expired. Please Login Again', 'status_code':401}, status=401)

            request.session['user_id'] = token_check.user_id
            
        except Exception as e:
            return JsonResponse({'status':'fail', 'message': 'Invalid token' + str(e), 'status_code':401}, status=401)

        response = self.get_response(request)
        return response