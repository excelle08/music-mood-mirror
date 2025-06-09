
from flask import Blueprint, request, jsonify
from lyrics import search

lyrics_api = Blueprint('lyrics_api', __name__)

@lyrics_api.route('/api/search', methods=['POST'])
def api_search():
    try:
        song_data = request.get_json()
        if not song_data:
            return jsonify({'error': 'Invalid JSON body'}), 400

        result = search(song_data)
        if result is None:
            return jsonify({'error': 'Could not parse song data'}), 400

        return jsonify(result.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
