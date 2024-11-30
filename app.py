import random
from flask import Flask, request, jsonify, abort
import json_parcer
import service as service


app = Flask(__name__)
FILE_PATH = 'data.json'
characters = json_parcer.load_data(FILE_PATH)
app.config.from_object('config')
# db = SQLAlchemy(app)


@app.route('/characters', methods=['GET'])
def get_characters():
    """
    Fetches a list of characters based on specified
    filters and pagination parameters.

    Args:
        None

    Returns:
        JSON response:
            - A list of characters matching the specified
                filters and pagination parameters.
            - An empty list if no characters match the criteria.
    """
    filters = []
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')
    limit = int(request.args.get('limit', 20))
    skip = int(request.args.get('skip', 0))

    for key, value in request.args.items():
        if key != "sort_by" or key != "sort_order" or key != "limit" or key != 'skip':
            filters.append({key: value})

    characters = service.characters_filter(filters)
    if sort_by:
        characters = service.characters_sort(characters, sort_order, sort_by)

    characters = characters.limit(limit).offset(skip).all()

    return jsonify([character.serialize() for character in characters])
        

@app.route('/characters/<int:id>', methods=['GET'])
def get_character_by_id(id):
    """
    Retrieves a character by its ID.

    Args:
        id: The ID of the character to retrieve.

    Returns:
        JSON response:
            - 200 OK: If the character is found and returned.
            - 404 Not Found: If the character is not found.
    """
    for character in characters:
        if character['id'] == id:
            return jsonify(character)
    abort(404, description="Character not found")


@app.route('/characters', methods=['POST'])
def create_character():
    """
    Creates a new character and adds it to the list of characters.

    Args:
        None

    Returns:
        JSON response:
            - 201 Created: If the character is created successfully.
            - 400 Bad Request: If required fields are missing or invalid.
    """
    data = request.get_json()
    # Validate required fields
    required_fields = ['name', 'house', 'animal', 'symbol', 'nickname', 'role', 'age', 'death', 'strength']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    # Validate data type for age
    try:
        age = int(data['age'])
        if age < 0:
            return jsonify({'error': 'Age must be a positive integer'}), 400
    except ValueError:
        return jsonify({'error': 'Age must be an integer'}), 400
    
    new_character = {
        "id": len(characters) + 1,
        "name": data.get('name', None),
        "house": data.get('house', None),
        "animal": data.get('animal', None),
        "symbol": data.get('symbol', None),
        "nickname": data.get('nickname', None),
        "role": data.get('role', None),
        "age": data.get('age', None),
        "death": data.get('death', None),
        "strength": data.get('strength', None)
    }
    characters.append(new_character)
    json_parcer.write_file(FILE_PATH, characters)

    return jsonify(new_character), 201


@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    """
    Updates an existing character by ID.

    Args:
        id: The ID of the character to update.

    Returns:
        JSON response:
            - 200 OK: If the character is updated successfully.
            - 404 Not Found: If the character is not found.
    """
    data = request.get_json()
    for character in characters:
        if character['id'] == id:
            if "name" in data:
                character['name'] = data['name']
                json_parcer.write_file(FILE_PATH, characters)
            if "house" in data:
                character['house'] = data['house']
                json_parcer.write_file(FILE_PATH, characters)
            if "animal" in data:
                character['animal'] = data['animal']
                json_parcer.write_file(FILE_PATH, characters)
            if "symbol" in data:
                character['symbol'] = data['symbol']
                json_parcer.write_file(FILE_PATH, characters)
            if "nickname" in data:
                character['nickname'] = data['nickname']
                json_parcer.write_file(FILE_PATH, characters)
            if "role" in data:
                character['role'] = data['role']
                json_parcer.write_file(FILE_PATH, characters)
            if "age" in data:
                character['age'] = data['age']
                json_parcer.write_file(FILE_PATH, characters)
            if "death" in data:
                character['death'] = data['death']
                json_parcer.write_file(FILE_PATH, characters)
            if "strength" in data:
                character['strength'] = data['strength']
                json_parcer.write_file(FILE_PATH, characters)
            response = {
                "id": character['id'],
                "name": character['name'],
                "house": character['house'],
                "animal": character['animal'],
                "symbol": character['symbol'],
                "nickname": character['nickname'],
                "role":character['role'],
                "age": character['age'],
                "death": character['death'],
                "strength": character['strength']
            }
            return jsonify(response), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404


@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    """
    Deletes a character by ID.

    Args:
        id: The ID of the character to delete.

    Returns:
        JSON response:
            - 200 OK: If the character is deleted successfully.
            - 404 Not Found: If the character is not found.
    """
    for character in characters:
        if character['id'] == id:
            characters.remove(character)
            json_parcer.write_file(FILE_PATH, characters)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    return jsonify({"message": f"Post with id {id} was not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)