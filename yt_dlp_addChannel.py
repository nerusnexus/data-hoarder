import yt_dlp

def fetch_channel_data(url):
    """
    Fetches channel metadata from YouTube using yt-dlp.
    Returns a dictionary of data or None if failed.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'dump_single_json': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        print(f"Error fetching channel data: {e}")
        return None
