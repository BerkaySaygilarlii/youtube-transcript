from flask import Flask, request, jsonify
from flask_cors import CORS  # CORS desteği için
import re

app = Flask(__name__)
CORS(app)  # Tüm kaynaklardan gelen isteklere izin verir

# YouTube video URL'lerinden video_id'yi çıkarmak için regex deseni
YOUTUBE_REGEX = re.compile(
    r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
)

def extract_video_id(url):
    match = YOUTUBE_REGEX.search(url)
    return match.group(1) if match else None

@app.route('/get_video_id', methods=['GET'])
def get_video_id():
    video_url = request.args.get('video_url')
    
    if video_url:
        video_id = extract_video_id(video_url)
        if video_id:
            return jsonify({"video_id": video_id})
        return jsonify({"error": "Invalid video URL."}), 400

    return jsonify({"error": "No video_url provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)
