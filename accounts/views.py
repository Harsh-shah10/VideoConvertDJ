from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import generate_login_token
import os
from rest_framework.views import APIView
from .tasks import convert_video_to_mp4
from .models import UploadedFile, ConvertedVideo, FileMetaData
from django.db import connection
import random
import string
# Create your views here.

# login view
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON data in request body', 'status_code': 400}, status=400)

        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return JsonResponse({'status': 'fail', 'message': 'Email and password are required', 'status_code': 400}, status=400)

        try:
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                return JsonResponse({'status': 'fail', 'message': 'Incorrect Password', 'status_code': 400}, status=400)
            
            token = generate_login_token(user.id)
            if token:
                return JsonResponse({'status': 'success', 'message': 'Logged In', 'token': token, 'status_code': 200}, status=200)
            else:
                return JsonResponse({'status': 'fail', 'message': 'Failed to generate token', 'status_code': 500}, status=500)

        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Account not found with this email', 'status_code': 404}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Error: {str(e)}', 'status_code': 500}, status=500)


#  user details api
@method_decorator(csrf_exempt, name='dispatch')
class UserDetailAPIView(View):
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'status': 'fail', 'message': 'User session not found', 'status_code': 400}, status=400)
            
            user_data = User.objects.get(id=user_id)
            data = {
                'fullname': user_data.fname,
                'email': user_data.email,
            }
            return JsonResponse({'status': 'success', 'message': 'Details fetched', 'data': data, 'status_code': 200}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'User not found', 'status_code': 404}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Something went wrong. Error: {str(e)}', 'status_code': 500}, status=500)


# signup view
@method_decorator(csrf_exempt, name='dispatch')
class UserSignupAPIView(View):
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON data in request body', 'status_code': 400}, status=400)

        # Validate payload fields
        required_fields = ['email', 'fullname', 'password']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'status': 'fail', 'message': f'Missing required field: {field}', 'status_code': 400}, status=400)

        email = data['email']
        fullname = data['fullname']
        password = data['password']

        try:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'fail', 'message': 'Email already exists', 'status_code': 400}, status=400)
            else:
                #Save new user to database
                acc = User(email=email, fname=fullname, password=make_password(password))
                acc.full_clean()  
                acc.save()
                
            return JsonResponse({'status': 'success', 'message': 'Account created', 'status_code': 200}, status=200)
        except ValidationError as e:
            return JsonResponse({'status': 'fail', 'message': e.message_dict, 'status_code': 400}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e), 'status_code': 500}, status=500)


# File upload API
@method_decorator(csrf_exempt, name='dispatch')
class FileUploadAPIView(APIView):
    
    def put(self, request, *args, **kwargs):
        try:
            user_id = request.session.get('user_id')        
            import os
            
            # Ensure 'file' key is present in request.FILES
            if 'file' not in request.FILES:
                return JsonResponse({'status': 'fail', 'message': 'No file found in request', 'status_code': 400}, status=400)

            # Get the uploaded file object
            uploaded_file = request.FILES['file']
            
            if "video" not in uploaded_file.content_type:
                return JsonResponse({'status': 'fail', 'message':'Only video files are allowed', 'status_code': 400}, status=400)

            filename = uploaded_file.name
            file_content = uploaded_file.read()

            random_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            file_name = f"{random_prefix}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename.replace('/', '')}"

            # Construct the file path within MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, f'users/', file_name)
            
            # Ensure the directory path exists; create if not
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the file to the specified path
            with open(file_path, 'wb+') as destination:
                destination.write(file_content)

            obj = UploadedFile.objects.create(file_location=f"users/{file_name}", uploaded_by_id=user_id)

            # Save metadata to FileMetaData table
            FileMetaData.objects.create(
                uploaded_file_id=int(obj.id),
                video_name=filename,
                video_size=len(file_content), 
                content_type=uploaded_file.content_type,
                created_by = user_id
            )
            
            file_extension = filename.split('.')[-1]
            
            # Using celery for tasks to run task in background
            try:
                convert_task = convert_video_to_mp4.delay(file_path, user_id, int(obj.id), file_extension)
            except:
                return JsonResponse({'status': 'fail', 'message': 'Please Upload valid video file', 'status_code': 400}, status=400)

            # Return success response with file details
            return JsonResponse({
                'data': 'Uploaded Successfully',
                'existingPath': file_name,
                'task_id': convert_task.id,
                'status': 'conversion started'
            })  

        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': f'Failed to upload file. Error: {str(e)}', 'status_code': 500}, status=500)
        

# For searching converted files 
class FileSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        size = request.GET.get('size', None)
        video_name = request.GET.get('video_name', None)
        user_id = request.session.get('user_id')  

        print(video_name)

        if not user_id:
            return JsonResponse({'status': 'fail', 'message': 'User not authenticated', 'status_code': 401}, status=401)

        query = """
            SELECT cf.uploaded_file_id, cf.file_location, fm.video_name, fm.video_size, fm.content_type 
            FROM converted_files cf 
            LEFT JOIN file_metadata fm 
            ON cf.uploaded_file_id = fm.uploaded_file_id
            WHERE cf.converted_by = %s
        """
        params = [user_id]
        
        # Add conditions if any of the filters are provided
        conditions = []
        if size:
            conditions.append("fm.video_size = %s")
            params.append(size)
        if video_name:
            conditions.append("fm.video_name LIKE %s")
            params.append(f'%{video_name}%')

        # Append conditions to the query using OR
        if conditions:
            query += " AND (" + " OR ".join(conditions) + ")"

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        results = [
            {
                'uploaded_file_id': row[0],
                'download_link': settings.MEDIA_URL + row[1],
                'video_name': row[2],
                'video_size': row[3],
                'content_type': row[4],
            }
            for row in rows
        ]

        return JsonResponse({'status': 'fail', 'results': results,  'status_code': 200}, status=200)

# List of all the files which have converted to mp4 for user
class ConvertedFilesListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')

        query = """
            SELECT cf.file_location as converted_file_locn, fm.video_name 
            FROM converted_files cf 
            LEFT JOIN file_metadata fm 
            ON fm.uploaded_file_id = cf.uploaded_file_id 
            WHERE cf.converted_by = %s
        """
        params = [user_id]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        results = [
            {
                'video_name': row[1],
                'download_link': settings.MEDIA_URL + row[0]
            }
            for row in rows
        ]

        return JsonResponse({'results': results}, status=200)
    

# logout user
class LogoutView(APIView):
    
    def post(self, request, *args, **kwargs):
        token_value = request.data.get('logout_token')
        if not token_value:
            return JsonResponse({'status': 'fail', 'message': 'Pass valid token', 'status_code': 400}, status=400)

        try:
            # Attempt to delete the token from the database
            token = Token.objects.get(unique_token=token_value)
            token.delete()
            return JsonResponse({'status': 'success', 'message': 'Logout successful', 'status_code': 200}, status=200)
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Token not found', 'status_code': 404}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'fail', 'message': str(e), 'status_code': 500}, status=404)