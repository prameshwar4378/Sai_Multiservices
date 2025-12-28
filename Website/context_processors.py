# your_app/context_processors.py
import re

def youtube_utils(request):
    """Add YouTube helper functions to all templates"""
    
    def extract_youtube_id(url):
        if not url:
            return ''
        url = url.split('&')[0]  # Remove parameters
        patterns = [
            r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/v\/)([a-zA-Z0-9_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ''
    
    def is_youtube_url(url):
        return url and ('youtube.com' in url or 'youtu.be' in url)
    
    def get_youtube_embed_url(url):
        video_id = extract_youtube_id(url)
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
        return url
    
    def get_youtube_thumbnail(video_id):
        if video_id:
            return f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg'
        return None
    
    return {
        'extract_youtube_id': extract_youtube_id,
        'is_youtube_url': is_youtube_url,
        'get_youtube_embed_url': get_youtube_embed_url,
        'get_youtube_thumbnail': get_youtube_thumbnail,
    }