import random
from flask import Flask, request, jsonify, abort
import json_parcer


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
    name = request.args.get('name')
    house = request.args.get('house')
    role = request.args.get('role')
    age_more_than = request.args.get('age_more_than')
    age_less_than = request.args.get('age_less_than')
    limit = int(request.args.get('limit', 20))
    skip = int(request.args.get('skip', 0))
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')

    filtered_characters = [char for char in characters if
                       (not name or char['name'].lower() == name.lower()) and
                       (not house or str(char['house']).lower().find(house.lower()) >= 0) and
                       (not role or char['role'].lower() == role.lower()) and
                       (not age_more_than or char['age'] >= int(age_more_than)) and
                       (not age_less_than or char['age'] <= int(age_less_than))]
    
    if sort_by:
        if sort_order == 'asc':
            filtered_characters.sort(key=lambda x: x[sort_by])
        else:
            filtered_characters.sort(key=lambda x: x[sort_by], reverse=True)

    # If no limit or skip is provided, select 20 random characters from the filtered list
    if not limit and not skip:
        paginated_characters = random.sample(filtered_characters, 20)
    else:
        # Apply pagination to the filtered list
        paginated_characters = filtered_characters[skip:skip + limit]

    return jsonify(paginated_characters)


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