import random
from flask import Flask, request, jsonify, abort
import json_parcer


app = Flask(__name__)

characters = json_parcer.load_data('data.json')

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

    This function implements a REST API endpoint to retrieve a paginated
    and filtered list of characters. It supports filtering by name,
    house, role, age range, and sorting by a specified field in ascending or descending order.
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

    This function searches for a character in the list of characters
    based on the provided ID. If the character is found,
    it returns the character's information as a JSON response.
    Otherwise, it returns a 404 Not Found error.
    """
    for character in characters:
        if character['id'] == id:
            return jsonify(character)
    abort(404, description="Character not found")


@app.route('/characters', methods=['GET','POST'])
def create_character():
    """
    Creates a new character and adds it to the list of characters.

    Args:
        None

    Returns:
        JSON response:
            - 201 Created: If the character is created successfully.
            - 400 Bad Request: If required fields are missing or invalid.

    This function handles the creation of new characters in the application.
    It validates the incoming JSON data, ensures that all required fields are
    present and have valid values, and then adds the new character to the in-memory list.
    The updated list is then written to a JSON file for persistence.
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
    json_parcer.write_file('data.json', characters)

    return jsonify(new_character), 201


@app.route()('/characters/<int:id>', methods=['PUT'])
def edit_character(id):
    pass
    
    

if __name__ == '__main__':
    app.run(debug=True)