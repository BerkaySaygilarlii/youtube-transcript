from flask import Flask, request, Response, jsonify
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi
import os

app = Flask(__name__)

@app.route("/get_transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({"error": "Please provide a video_id parameter"}), 400

    try:
        # Videodan transkripti al
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Her text'i satırlara ayırarak döndür
        transcript_text = "\n".join([entry['text'] for entry in transcript])

        # Basit bir metin çıktısı döndür
        return Response(transcript_text, content_type='text/plain'), 200

    except TranscriptsDisabled:
        return jsonify({"error": "Subtitles are disabled for this video."}), 400

    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Heroku'nun sağladığı PORT'u kullan
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
