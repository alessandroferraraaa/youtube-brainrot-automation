import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube():
    """Upload video su YouTube"""
    
    # Credenziali OAuth
    credentials = Credentials(
        token=os.environ.get('YOUTUBE_ACCESS_TOKEN'),
        refresh_token=os.environ.get('YOUTUBE_REFRESH_TOKEN'),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ.get('YOUTUBE_CLIENT_ID'),
        client_secret=os.environ.get('YOUTUBE_CLIENT_SECRET')
    )
    
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Metadata video
    request_body = {
        'snippet': {
            'title': '🔥 Crazy Story You Won\'t Believe! #shorts',
            'description': 'Follow for more viral content! 🚀\n\n#brainrot #viral #shorts',
            'tags': ['shorts', 'viral', 'story', 'brainrot'],
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    # Upload
    media = MediaFileUpload('final_video.mp4', chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    
    response = request.execute()
    
    video_id = response['id']
    print(f"✅ Video caricato: https://youtube.com/shorts/{video_id}")
    
    return video_id

if __name__ == "__main__":
    upload_to_youtube()