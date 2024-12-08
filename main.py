from flask import Flask, request, render_template, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/get_transcript", methods=["POST"])
def get_transcript():
    video_url = request.form.get('video_url')

    # URL'den video ID'sini çıkarma (https://www.youtube.com/watch?v=VIDEO_ID)
    video_id = video_url.split("v=")[-1].split("&")[0]  # URL'den video ID'sini almak

    if not video_id:
        return jsonify({"error": "Please provide a valid YouTube URL."}), 400

    try:
        # Videodan transkripti al
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Her text'i satırlara ayırarak döndür
        transcript_text = "\n".join([entry['text'] for entry in transcript])

        return render_template("home.html", transcript=transcript_text)

    except TranscriptsDisabled:
        return render_template("home.html", error="Subtitles are disabled for this video.")

    except NoTranscriptFound:
        return render_template("home.html", error="No transcript found for this video.")

    except Exception as e:
        return render_template("home.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
