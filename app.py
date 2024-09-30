from flask import Flask, render_template, request
from video import fetch_formats  # Assuming this function is implemented in video.py for fetching formats
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_formats', methods=['POST'])
def get_formats():
    video_url = request.form.get('video_url')
    try:
        # Fetch available formats for the given URL
        formats = fetch_formats(video_url)
        if formats:
            return render_template('format_options.html', formats=formats, video_url=video_url)
        else:
            return render_template('error.html', message="No valid formats found.")
    except Exception as e:
        print(f"Error fetching formats: {e}")
        return render_template('error.html', message="Error fetching formats.")

@app.route('/download', methods=['POST'])
def download():
    format_id = request.form.get('format_id')
    video_url = request.form.get('url')
    
    try:
        # Download video with both audio and video (for MP4)
        ydl_opts = {
            'format': format_id + "+bestaudio/best",  # Combine video and audio for MP4
            'merge_output_format': 'mp4',  # Output as MP4
            'outtmpl': '%(title)s.%(ext)s',  # Name of the downloaded file
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        return render_template('success.html', message="Download completed successfully!")
    
    except Exception as e:
        print(f"Error downloading file: {e}")
        return render_template('error.html', message="Error downloading file.")

if __name__ == "__main__":
    app.run(debug=True)
