import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def extract_video_id(video_url):
    """Extracts video ID from various YouTube URL formats."""
    parsed_url = urlparse(video_url)
    query_params = parse_qs(parsed_url.query)

    # Klasik URL formatı: https://www.youtube.com/watch?v=VIDEO_ID
    if 'v' in query_params:
        return query_params['v'][0]

    # Kısa URL formatı: https://youtu.be/VIDEO_ID
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path.lstrip('/')

    # Embed URL formatı: https://www.youtube.com/embed/VIDEO_ID
    if parsed_url.path.startswith('/embed/'):
        return parsed_url.path.split('/embed/')[1]

    raise ValueError("Invalid YouTube URL. Could not find video ID.")

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    """Fetches the transcript of a given YouTube video URL."""
    video_url = request.args.get('video_url')

    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400

    try:
        # Extract video ID from the URL
        video_id = extract_video_id(video_url)
        
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
