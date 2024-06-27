from celery import shared_task
import time
from django.conf import settings
from moviepy.editor import VideoFileClip
from .models import ConvertedVideo

@shared_task
def test_celery():
    time.sleep(10)
    return 'Task executed !!'


@shared_task
def convert_video_to_mp4(file_path, user_id, org_file_id, file_extension):
    try:
        video = VideoFileClip(file_path)
        mp4_file_path = file_path.replace('.'+file_extension, 'converted.mp4') 
        video.write_videofile(mp4_file_path)
        
        full_path = str(mp4_file_path)
        index = full_path.find('users/')

        # Save converted video information to ConvertedVideo model
        ConvertedVideo.objects.create(
            uploaded_file_id = org_file_id,
            file_location= full_path[index:],
            converted_by=user_id, 
        )
        
        return True
    except Exception as e:
        raise e