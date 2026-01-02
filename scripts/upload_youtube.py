import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube():
    """Upload brainrot short video to YouTube"""
    
    print("Uploading to YouTube...")
    
    client_id = os.getenv('YOUTUBE_CLIENT_ID')
    client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
    
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials")
    
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )
    
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Load brainrot short script
    with open('brainrot_short.json', 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    title = script_data['title'][:100]
    
    # Create description
    characters = ', '.join(script_data.get('characters', []))
    description = f"Brainrot short featuring: {characters}\n\n"
    description += f"Duration: {script_data.get('total_duration', 45)}s\n\n"
    description += "#Shorts #Brainrot #" + " #".join(script_data.get('tags', [])[:5])
    
    tags = script_data.get('tags', [])[:10]
    tags.extend(['brainrot', 'shorts', 'memes'])
    
    body = {
        'snippet': {
            'title': title,
            'description': description[:5000],
            'tags': tags,
            'categoryId': '24'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(
        'brainrot_short.mp4',
        mimetype='video/mp4',
        resumable=True,
        chunksize=1024*1024
    )
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    print("Uploading video...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"Upload progress: {progress}%")
    
    video_id = response['id']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"Video uploaded successfully!")
    print(f"Video URL: {video_url}")
    print(f"Video ID: {video_id}")
    
    return video_url

if __name__ == "__main__":
    upload_to_youtube()
