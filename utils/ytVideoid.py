import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    """
    # Handle youtu.be short URLs
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0].split("&")[0]
    
    # Handle youtube.com URLs
    if "youtube.com" in url:
        parsed_url = urlparse(url)
        
        # Extract from query parameters (?v=VIDEO_ID)
        if "watch" in parsed_url.path:
            query_params = parse_qs(parsed_url.query)
            if "v" in query_params:
                return query_params["v"][0]
        
        # Extract from embed URLs (/embed/VIDEO_ID)
        if "/embed/" in parsed_url.path:
            return parsed_url.path.split("/embed/")[1].split("?")[0]
        
        # Extract from /v/ URLs
        if "/v/" in parsed_url.path:
            return parsed_url.path.split("/v/")[1].split("?")[0]
    
    # If no pattern matches, try regex as fallback
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    
    raise ValueError("Could not extract video ID from URL")