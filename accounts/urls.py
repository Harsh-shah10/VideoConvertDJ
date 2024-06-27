from django.urls import path
from .views import UserSignupAPIView, UserLoginAPIView, UserDetailAPIView, FileUploadAPIView, FileSearchAPIView, ConvertedFilesListAPIView, LogoutView

urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('user_details/', UserDetailAPIView.as_view(), name='user_details'),
    path('upload/', FileUploadAPIView.as_view(), name='file_upload'),
    path('search/', FileSearchAPIView.as_view(), name='file_search'),
    path('converted-files/', ConvertedFilesListAPIView.as_view(), name='converted_files_list'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
