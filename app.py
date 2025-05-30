from flask import Flask, render_template, request, jsonify
from ytmusicapi import YTMusic

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    results = ytmusic.search(query, filter='songs')
    songs = []
    for r in results[:10]:
        songs.append({
            'title': r['title'],
            'videoId': r['videoId'],
            'artists': ', '.join([a['name'] for a in r['artists']]) if r.get('artists') else '',
            'thumbnail': r['thumbnails'][0]['url'] if r.get('thumbnails') else '',
        })
    return jsonify(songs)

if __name__ == '__main__':
    app.run(debug=True)