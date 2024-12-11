from flask import Flask, request, jsonify, abort
import service as service
import database
from schemas import CharacterUpdate, CharacterCreate
from pydantic import ValidationError
from config import Config


# Inizialisation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
database.create_database(app)


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
    sort_order = request.args.get('sort_order')
    limit = int(request.args.get('limit', 20))
    skip = int(request.args.get('skip', 0))

    for key, value in request.args.items():
        if key not in ("sort_by", "sort_order", "limit", "skip"):
            filters.append({key: value})
    # Call the filtering for house and strength filters inside the function
    # Call other filters
    characters = service.other_filters(service.house_strength_filters(filters), filters)

    if sort_by:
        characters = service.characters_sort(characters, sort_order, sort_by)

    characters = characters.limit(limit).offset(skip).all()
    if not characters:
        abort(404, description='Not Found: The requested page or resource could not be found')

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

    Request Body:
        A JSON object containing the following fields:
        - `name` (str, required): The name of the character.
        - `animal` (str, optional): The animal associated with the character.
        - `symbol` (str, optional): The symbol of the character.
        - `nickname` (str, optional): The nickname of the character.
        - `role` (str, optional): The role of the character.
        - `age` (int, required): The age of the character.
        - `death` (int, optional): The year of the character's death.
        - `house` (int, required): The ID of the house the character belongs to.
        - `strength` (int, required): The ID of the strength associated with the character.

    Returns:
        - 201 Created: If the character is created successfully.
        - 400 Bad Request: If the request body is invalid or missing required fields.
        - 500 Internal Server Error: If an unexpected error occurs.
    """
    try:
        character_data = CharacterCreate(**request.json)
        new_character = service.create_character(character_data.dict())
        return jsonify(new_character), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    """
    Updates an existing character.

    Args:
        id (int): The ID of the character to update.

    Returns:
        JSON response:
            - 200 OK: If the character is updated successfully.
            - 400 Bad Request: If the request data is invalid or missing required fields.
            - 404 Not Found: If the character with the given ID is not found.
            - 500 Internal Server Error: If an unexpected error occurs during the update process.
    """
    character = service.get_character(id)
    if not character:
        abort(404, description="Character not found")

    try:
        updated_data = CharacterUpdate(**request.get_json())
        updated_character = service.update_character(updated_data, id)
        return jsonify(updated_character), 200
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
            - 500 Internal Server Error: If an unexpected error occurs.
    """
    character = service.get_character(id)
    if not character:
        abort(404, description="Character not found")
    try:
        service.delete_character(id)
        return jsonify({'message': 'Character deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Endpoints to add house and strength
@app.route('/characters/house', methods=['POST'])
def add_character_house():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': f'Missing field: {'name'}'}), 400
    new_house = service.add_house(data)
    if new_house:
        return jsonify(new_house), 201
    return jsonify(new_house), 400


@app.route('/characters/strength', methods=['POST'])
def add_character_strength():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': f'Missing field: {'name'}'}), 400
    new_strength = service.add_strength(data)
    if new_strength:
        return jsonify(new_strength), 201
    return jsonify(new_strength), 400


if __name__ == '__main__':
    app.run(debug=True)