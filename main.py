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

        return jsonify({"transcript": transcript_text})

    except TranscriptsDisabled:
        return jsonify({"error": "Subtitles are disabled for this video."}), 400

    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
