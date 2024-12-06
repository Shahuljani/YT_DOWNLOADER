from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os

app = Flask(__name__, template_folder='templates')  # Specify the template folder

DOWNLOAD_DIR = "downloads"  # Directory to save downloaded videos
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Set the path to ffmpeg if it's not in your system's PATH
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-7.1-full_build\bin\ffmpeg.exe"  # Update this path to where ffmpeg is located

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/download', methods=['POST'])
def download_video():
    try:
        # Get the video URL from the frontend (received as JSON)
        video_url = request.json.get('url')
        if not video_url:
            return jsonify({"error": "No URL provided"}), 400

        # Configure yt-dlp options
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',  # Save format
            'format': 'bestvideo+bestaudio/best',           # Best quality (video + audio)
            'merge_output_format': 'mp4',                   # Specify the output format (mp4)
            'ffmpeg_location': FFMPEG_PATH,                 # Path to ffmpeg executable
            'noplaylist': True                             # Avoid downloading playlists
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
