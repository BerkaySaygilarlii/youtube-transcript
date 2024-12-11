import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_youtube_id(url):
    # Extract video ID from YouTube URL
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    return video_id.group(1) if video_id else None

def process_transcript(video_id):
    proxy_address=os.environ.get("PROXY")
    transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies = {"http": proxy_address,"https": proxy_address})
    full_text = ' '.join([entry['text'] for entry in transcript])
    return full_text

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    """Fetches the transcript of a given YouTube video URL."""
    youtube_url = request.json.get('url')
    

    if not youtube_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        # Extract video ID from the URL
        video_id = get_youtube_id(youtube_url)
        
        # Fetch the transcript using the YouTube Transcript API
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Optionally format the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return jsonify({"transcript": formatted_transcript}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to fetch transcript: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Heroku port
    app.run(host="0.0.0.0", port=port, debug=False)
