import yt_dlp

def fetch_formats(video_url):
    ydl_opts_info = {
        'quiet': True,
    }

    # Fetch video information
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict['formats']

    allowed_qualities = ['144p', '360p', '480p', '720p', '1080p']
    video_formats = {}
    audio_formats = []

    # Separate formats into video and audio, filter video formats to get the largest one per resolution
    for fmt in formats:
        if 'height' in fmt:
            quality = f"{fmt['height']}p"
            size = fmt.get('filesize', fmt.get('filesize_approx', None))

            # Only consider formats with an allowed quality and known size
            if quality in allowed_qualities and size is not None:
                size_mb = size / (1024 * 1024)

                # Store only the largest format for each resolution
                if quality not in video_formats or size_mb > video_formats[quality]['size_mb']:
                    video_formats[quality] = {
                        'format_id': fmt['format_id'],
                        'quality': quality,
                        'size': f"{size_mb:.2f} MB",
                        'size_mb': size_mb  # Keep size in MB for comparison
                    }

        # For audio (MP3)
        if fmt.get('acodec', '') != 'none' and fmt.get('vcodec') == 'none':
            size = fmt.get('filesize', fmt.get('filesize_approx', None))
            if size is not None:
                size_mb = size / (1024 * 1024)
                audio_formats.append({
                    'format_id': fmt['format_id'],
                    'size': f"{size_mb:.2f} MB"
                })

    # Return the best video format for each resolution and all audio formats
    return {
        'video_formats': list(video_formats.values()),  # Only the largest format for each resolution
        'audio_formats': audio_formats
    }
