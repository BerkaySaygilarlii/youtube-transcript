import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

app = Flask(__name__)
CORS(app)

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    # Video ID'sini URL'den al
    video_url = request.args.get('video_url')  # video_url parametresini alıyoruz
    
    if not video_url:
        return jsonify({"error": "Video URL is required"}), 400
    
    # URL'den video ID'sini çıkar
    video_id = video_url.split("v=")[-1].split("&")[0]
    
    try:
        # Transcript'i al
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Transkripti formatla (isteğe bağlı)
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return jsonify({"transcript": formatted_transcript}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Heroku port
    app.run(host="0.0.0.0", port=port , debug=False)
