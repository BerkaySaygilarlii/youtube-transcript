from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route("/get_transcript", methods=["GET"])
def get_transcript():
    # URL query parametresi üzerinden video_id alıyoruz
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({"error": "Please provide a valid video ID."}), 400

    try:
        # Videodan transkripti al
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Her text'i satırlara ayırarak döndür
        transcript_text = "\n".join([entry['text'] for entry in transcript])

        return jsonify({"transcript": transcript_text})

    except TranscriptsDisabled:
        return jsonify({"error": "Subtitles are disabled for this video."})

    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
ß