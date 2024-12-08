from flask import Flask, request, jsonify, abort
import json_parcer
import service as service
import database
from schemas import CharacterUpdate
from pydantic import ValidationError
from config import Config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
database.create_database(app)
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

    return jsonify([character.to_dict() for character in characters])
        

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
    character_data = service.get_character(id)
    if character_data:
        return jsonify(character_data)
    else:
        abort(404, description="Character not found")


@app.route('/characters', methods=['POST'])
def create_character():
    """
    Creates a new character.

    Args: (data received from the request body)
        name (str): The name of the character.
        animal (str): The animal associated with the character.
        symbol (str): The symbol of the character.
        nickname (str): The nickname of the character.
        role (str): The role of the character.
        age (int): The age of the character.
        death (int, optional): The year of the character's death (if applicable).
        house_id (int): The ID of the house the character belongs to.
        strength_id (int): The ID of the strength associated with the character.

    Returns:
        JSON response:
            - 201 Created: If the character is created successfully.
            - 400 Bad Request: If required data is missing or invalid.
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
    new_character = service.create_character(data)
    if new_character:
        return jsonify(new_character), 201
    return jsonify(new_character), 400


@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    """
    Updates an existing character.

    Args:
        id (int): The ID of the character to update.
        data (dict): The updated character data (received from the request body).

    Returns:
        JSON response:
            - 200 OK: If the character is updated successfully.
            - 400 Bad Request: If required data is missing or invalid.
            - 404 Not Found: If the character is not found.
    """
    character = service.get_character(id)
    if not character:
        abort(404, description="Character not found")

    try:
        updated_data = CharacterUpdate(**request.get_json())
    except ValidationError as e:
        return jsonify({'problem1=error': str(e)}), 400

    try:
        updated_character = service.update_character(updated_data, id)
    except Exception as e:
        return jsonify({'problem2=error': str(e)}), 400

    if updated_character:
        return jsonify(updated_character), 200
    else:
        return jsonify({'problem3=error': 'Failed to update character'}), 400 


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