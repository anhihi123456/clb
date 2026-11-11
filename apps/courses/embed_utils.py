"""
Utility module for extracting, normalizing, and safely constructing embed URLs
for YouTube videos, Google Drive files (PDFs/Slides), Google Docs, and Google Forms.
Prevents raw HTML injection (XSS) and ensures only permitted origins can be embedded.
"""

import re
from urllib.parse import urlparse, parse_qs


class EmbedParseError(Exception):
    """Custom exception raised when an embed link cannot be parsed or is disallowed."""
    pass


def extract_youtube_info(raw_url: str):
    """
    Extracts YouTube Video ID and generates a standardized embed URL.
    Supports:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://www.youtube.com/embed/VIDEO_ID
      - https://www.youtube.com/shorts/VIDEO_ID
      - Raw 11-character video ID
    """
    raw_url = raw_url.strip()

    # If teacher pasted raw iframe HTML, extract src
    iframe_match = re.search(r'src=["\']([^"\']+)["\']', raw_url)
    if iframe_match:
        raw_url = iframe_match.group(1)

    # Check if input is directly an 11-char ID
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', raw_url):
        video_id = raw_url
        return {
            'provider': 'youtube',
            'external_id': video_id,
            'embed_url': f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&rel=0",
            'preview_url': f"https://www.youtube.com/watch?v=dQw4w9WgXcQ" if not video_id else f"https://www.youtube.com/watch?v={video_id}",
        }

    parsed = urlparse(raw_url)
    hostname = (parsed.hostname or '').lower().replace('www.', '')

    video_id = None
    if hostname in ('youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            qs = parse_qs(parsed.query)
            if 'v' in qs and qs['v']:
                video_id = qs['v'][0]
        elif parsed.path.startswith('/embed/'):
            video_id = parsed.path.split('/')[2]
        elif parsed.path.startswith('/shorts/'):
            video_id = parsed.path.split('/')[2]
    elif hostname == 'youtu.be':
        # Path is /VIDEO_ID
        video_id = parsed.path.lstrip('/')
        if '?' in video_id:
            video_id = video_id.split('?')[0]

    if video_id and re.fullmatch(r'[a-zA-Z0-9_-]{11}', video_id):
        return {
            'provider': 'youtube',
            'external_id': video_id,
            'embed_url': f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&rel=0",
            'preview_url': f"https://www.youtube.com/watch?v={video_id}",
        }

    raise EmbedParseError("Đường dẫn YouTube không hợp lệ. Vui lòng dán liên kết dạng 'https://www.youtube.com/watch?v=...' hoặc 'https://youtu.be/...'")


def extract_gdrive_info(raw_url: str):
    """
    Extracts Google Drive file ID, Google Slides ID, or Google Docs ID
    and generates a standardized embed preview URL.
    Supports:
      - https://drive.google.com/file/d/FILE_ID/view
      - https://drive.google.com/open?id=FILE_ID
      - https://docs.google.com/presentation/d/PRESENTATION_ID/edit
      - https://docs.google.com/document/d/DOC_ID/edit
    """
    raw_url = raw_url.strip()

    # If teacher pasted raw iframe HTML, extract src
    iframe_match = re.search(r'src=["\']([^"\']+)["\']', raw_url)
    if iframe_match:
        raw_url = iframe_match.group(1)

    parsed = urlparse(raw_url)
    hostname = (parsed.hostname or '').lower()

    # 1. Google Drive File (PDF, Slides, Video upload)
    if 'drive.google.com' in hostname:
        # /file/d/FILE_ID/...
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', parsed.path)
        if match:
            file_id = match.group(1)
            return {
                'provider': 'gdrive',
                'external_id': file_id,
                'embed_url': f"https://drive.google.com/file/d/{file_id}/preview",
                'preview_url': f"https://drive.google.com/file/d/{file_id}/view",
            }
        # ?id=FILE_ID
        qs = parse_qs(parsed.query)
        if 'id' in qs and qs['id']:
            file_id = qs['id'][0]
            return {
                'provider': 'gdrive',
                'external_id': file_id,
                'embed_url': f"https://drive.google.com/file/d/{file_id}/preview",
                'preview_url': f"https://drive.google.com/file/d/{file_id}/view",
            }

    # 2. Google Slides
    if 'docs.google.com' in hostname and '/presentation/' in parsed.path:
        match = re.search(r'/presentation/d/([a-zA-Z0-9_-]+)', parsed.path)
        if match:
            presentation_id = match.group(1)
            return {
                'provider': 'gslides',
                'external_id': presentation_id,
                'embed_url': f"https://docs.google.com/presentation/d/{presentation_id}/embed?start=false&loop=false&delayms=3000",
                'preview_url': f"https://docs.google.com/presentation/d/{presentation_id}/edit",
            }

    # 3. Google Docs
    if 'docs.google.com' in hostname and '/document/' in parsed.path:
        match = re.search(r'/document/d/([a-zA-Z0-9_-]+)', parsed.path)
        if match:
            doc_id = match.group(1)
            return {
                'provider': 'gdocs',
                'external_id': doc_id,
                'embed_url': f"https://docs.google.com/document/d/{doc_id}/preview",
                'preview_url': f"https://docs.google.com/document/d/{doc_id}/edit",
            }

    raise EmbedParseError("Đường dẫn Google Drive không hợp lệ. Vui lòng dán liên kết dạng 'https://drive.google.com/file/d/.../view' hoặc Google Slides/Docs.")


def extract_gform_info(raw_url: str):
    """
    Extracts Google Form embed URL from a shareable link or embed snippet.
    """
    raw_url = raw_url.strip()
    iframe_match = re.search(r'src=["\']([^"\']+)["\']', raw_url)
    if iframe_match:
        raw_url = iframe_match.group(1)

    parsed = urlparse(raw_url)
    hostname = (parsed.hostname or '').lower()

    if 'docs.google.com' in hostname and '/forms/' in parsed.path:
        # Standardize to have ?embedded=true
        base_path = parsed.path
        if not base_path.endswith('/viewform'):
            base_path = re.sub(r'/(edit|viewform).*$', '/viewform', base_path)
            if not base_path.endswith('/viewform'):
                base_path = base_path.rstrip('/') + '/viewform'
        return {
            'provider': 'gforms',
            'external_id': base_path,
            'embed_url': f"https://docs.google.com{base_path}?embedded=true",
            'preview_url': f"https://docs.google.com{base_path}",
        }

    raise EmbedParseError("Đường dẫn Google Forms không hợp lệ. Vui lòng dán liên kết dạng 'https://docs.google.com/forms/d/e/.../viewform'")


def parse_media_url(raw_url: str, expected_type: str = None):
    """
    Auto-detects the provider or parses according to expected_type ('video', 'document', 'quiz').
    Returns dict: {'provider': ..., 'external_id': ..., 'embed_url': ..., 'preview_url': ...}
    """
    if not raw_url or not raw_url.strip():
        raise EmbedParseError("Vui lòng cung cấp đường dẫn tài liệu hoặc video.")

    raw_url = raw_url.strip()

    if expected_type == 'video' or 'youtube' in raw_url.lower() or 'youtu.be' in raw_url.lower():
        return extract_youtube_info(raw_url)
    
    if expected_type == 'document' or 'drive.google.com' in raw_url.lower() or ('docs.google.com' in raw_url.lower() and ('presentation' in raw_url.lower() or 'document' in raw_url.lower())):
        return extract_gdrive_info(raw_url)

    if expected_type == 'quiz' or 'forms' in raw_url.lower():
        return extract_gform_info(raw_url)

    # Auto detect
    try:
        return extract_youtube_info(raw_url)
    except EmbedParseError:
        pass

    try:
        return extract_gdrive_info(raw_url)
    except EmbedParseError:
        pass

    try:
        return extract_gform_info(raw_url)
    except EmbedParseError:
        pass

    raise EmbedParseError(
        "Không nhận diện được dịch vụ hỗ trợ. Hệ thống chỉ hỗ trợ liên kết từ YouTube (video), "
        "Google Drive (PDF/Slide), Google Docs/Slides hoặc Google Forms."
    )

