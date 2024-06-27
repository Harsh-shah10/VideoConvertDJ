from .models import *
from datetime import datetime, timedelta
from django.conf import settings

def generate_login_token(user_id):
    try:
        Token.objects.filter(user_id=user_id).delete()
        
        login_token = Token()

        import jwt
        payload = ({'exp': datetime.now() + timedelta(hours=1),  'iat': datetime.now() })

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        
        generated_token = token.split('.')[2]
        expiry_hrs = 4 # setting 4 hours expiry by default 

        login_token.user_id = user_id
        login_token.unique_token = generated_token
        login_token.expiry = datetime.now() + timedelta(hours=expiry_hrs)
        login_token.status = "Active"
        login_token.save()
        return generated_token

    except Exception as e:
        # import sys, os
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno, str(e))
        return False
