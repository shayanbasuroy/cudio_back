from flask import Flask, render_template, request, jsonify
from ytmusicapi import YTMusic
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS globally so frontend can access API cross-origin

ytmusic = YTMusic()

@app.route('/')
def index():
    # Make sure index.html is in templates/ folder
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()

    if not query:
        return jsonify([])  # Return empty list if no query

    results = ytmusic.search(query, filter='songs')
    songs = []

    for r in results[:10]:
        songs.append({
            'title': r.get('title', 'Unknown Title'),
            'videoId': r.get('videoId', ''),
            'artists': ', '.join([a['name'] for a in r.get('artists', [])]) if r.get('artists') else '',
            'thumbnail': r['thumbnails'][0]['url'] if r.get('thumbnails') else '',
        })

    return jsonify(songs)

if __name__ == '__main__':
    # Run on 0.0.0.0 so Render.com can access it, port 5000 default
    app.run(host='0.0.0.0', port=5000, debug=True)
