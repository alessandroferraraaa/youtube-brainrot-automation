import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube():
    """Upload video to YouTube"""
    
    print("📤 Uploading to YouTube...")
    
    # Get credentials from environment
    client_id = os.getenv('YOUTUBE_CLIENT_ID')
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials in environment variables")
    
    # Create credentials
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Build YouTube service
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Load script for title and description
    with open('script.json', 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    title = script_data['title'][:100]  # YouTube title max 100 chars
    description = f"{script_data['story'][:500]}\n\n#Shorts #Story #Brainrot"
    tags = script_data.get('tags', [])[:10]  # Max 10 tags
    
    # Upload video
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '24'  # Entertainment
        },
        'status': {
            'privacyStatus': 'public',  # or 'private' for testing
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(
        'final_video.mp4',
        mimetype='video/mp4',
        resumable=True,
        chunksize=1024*1024  # 1MB chunks
    )
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    print("⏳ Uploading video...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"📊 Upload progress: {progress}%")
    
    video_id = response['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"✅ Video uploaded successfully!")
    print(f"🎬 Video URL: {video_url}")
    print(f"📺 Video ID: {video_id}")
    
    return video_url

if __name__ == "__main__":
    upload_to_youtube()
