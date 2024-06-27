from django.db import models

# Create your models here.
class User(models.Model):
    ACCOUNT_STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]
    
    fname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    account_status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICES,
        default='Active',
        max_length=255
    )
    
    class Meta:
        db_table = 'users'
        managed = False  
        
        
# For token creation 
class Token(models.Model):
    STATUS_CHOICES =  [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]
    
    user_id = models.IntegerField()
    unique_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    
    class Meta:
        db_table = 'token'
        managed = False  
    
    
class UploadedFile(models.Model):
    file_location = models.CharField(max_length=255)
    uploaded_by_id =  models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uploaded_files'
        managed = False  
        
class ConvertedVideo(models.Model):
    uploaded_file_id = models.IntegerField() # FK of Uploaded file
    file_location = models.CharField(max_length=255)
    converted_by = models.IntegerField()
    converted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'converted_files'
        managed = False  
    

class FileMetaData(models.Model):
    uploaded_file_id = models.IntegerField()
    video_name = models.CharField(max_length=255)
    video_size = models.PositiveIntegerField()  # Assuming video size in bytes
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField()  # Assuming this is the user_id

    class Meta:
        db_table = 'file_metadata'
        managed = False  
        
    
    
