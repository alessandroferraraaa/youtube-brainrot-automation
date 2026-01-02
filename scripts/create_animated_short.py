import os
import json
import asyncio
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import requests

def generate_scene_with_ai(scene_description, duration):
    """
    Generate video clip using AI (Runway ML, Luma AI, or similar)
    For now, we'll use static images + effects as placeholder
    """
    print(f"  Generating scene: {scene_description[:50]}...")
    
    # TODO: Integrate with Runway ML API or Luma AI
    # For now: download placeholder from Pexels or use solid color
    
    # Placeholder: create colored background with text
    from moviepy import ColorClip
    
    clip = ColorClip(size=(1080, 1920), color=(20, 20, 20), duration=duration)
    
    # Add text overlay
    txt = TextClip(
        text=scene_description[:100],
        font='Arial-Bold',
        font_size=60,
        color='white',
        size=(1000, None),
        method='caption'
    )
    txt = txt.with_position('center').with_duration(duration)
    
    return CompositeVideoClip([clip, txt])

async def generate_voiceover_for_scene(text, voice, output_file):
    """Generate voiceover for a single scene"""
    communicate = edge_tts.Communicate(text, voice, rate="+10%")
    await communicate.save(output_file)
    return output_file

def create_animated_short():
    """Create animated brainrot short video"""
    
    print("🎬 Creating animated brainrot short...")
    
    with open('brainrot_short.json', 'r') as f:
        script = json.load(f)
    
    clips = []
    
    for i, scene in enumerate(script['scenes']):
        print(f"\n📹 Scene {i+1}/{len(script['scenes'])}")
        
        # Generate voiceover
        voice_file = f"scene_{i}_voice.mp3"
        asyncio.run(generate_voiceover_for_scene(
            scene['dialogue'],
            scene.get('voice', 'en-US-GuyNeural'),
            voice_file
        ))
        
        # Load audio
        audio = AudioFileClip(voice_file)
        duration = audio.duration
        
        # Generate video clip (AI generation here)
        video_description = f"{scene['character']}: {scene['action']}"
        video = generate_scene_with_ai(video_description, duration)
        
        # Combine
        video = video.with_audio(audio)
        clips.append(video)
    
    # Concatenate all scenes
    print("\n🎞️ Combining scenes...")
    final = concatenate_videoclips(clips, method="compose")
    
    # Export
    print("💾 Exporting...")
    final.write_videofile(
        'brainrot_short.mp4',
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='fast',
        threads=4
    )
    
    print("✅ Brainrot short created!")
    
    # Cleanup
    for clip in clips:
        clip.close()
    
    return 'brainrot_short.mp4'

if __name__ == "__main__":
    create_animated_short()
