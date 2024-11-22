from flask import Flask, request, jsonify, abort
import json_parcer


app = Flask(__name__)

characters = json_parcer.load_data('data.json')

@app.route('/characters', methods=['GET'])
def get_characters():
    """
    Fetch all characters (with Pagination)
    
    """
    limit = int(request.args.get('limit', 20))
    skip = int(request.args.get('skip', 0))

    paginated_characters = characters[skip:skip + limit]

    return jsonify(paginated_characters)


@app.route('/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):
    """
    Fetch a specific character by ID
    """
    for character in characters:
        if character['id'] == id:
            return jsonify(character)
    abort(404, description="Character not found")


if __name__ == '__main__':
    app.run(debug=True)