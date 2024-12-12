from flask import Flask, request, jsonify, abort
import jwt
from pydantic import ValidationError
from datetime import datetime, timedelta
from functools import wraps
import service as service
import database
from schemas import CharacterUpdate, CharacterCreate
from config import Config


# Inizialisation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
database.create_database(app)


# In-memory user database (replace with a database query)
users = [
    {'username': 'user1', 'password': 'password1', 'role': 'user'},
    {'username': 'admin', 'password': 'adminpassword', 'role': 'admin'},
]


# Authentication & Authorization
def generate_jwt(username, role):
    """
    Generates a JSON Web Token (JWT) containing user information.

    Args:
        username (str): The username of the authenticated user.
        role (str): The user's role (e.g., "admin", "user").

    Returns:
        str: The encoded JWT token.

    Raises:
        ValueError: If a secret key is not configured or invalid data is provided.
    """
    if not Config.JWT_SECRET_KEY:
        raise ValueError("JWT secret key is not configured.")

    payload = {
        'username': username,
        'role': role,
        'exp': datetime.now() + timedelta(days=1)  # Set appropriate expiration time
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')


def decode_jwt(token):
    """
    Decodes a JWT token and retrieves user information if valid.

    Args:
        token (str): The encoded JWT token.

    Returns:
        dict | None: The decoded user information if the token is valid,
            otherwise None.

    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authenticate(username, password):
    """
    Authenticates a user based on username and password.

    **Important:** This is a simplified in-memory authentication example.
    For production use, implement secure password hashing (e.g., bcrypt)
    and store hashed passwords in a database.

    Args:
        username (str): The username to authenticate.
        password (str): The user's password for authentication.

    Returns:
        str | None: The user's role if authentication is successful,
            otherwise None.
    """
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user['role']
    return None


def protect_endpoint(func):
    """
    Decorator that verifies JWT authorization for a protected endpoint.

    Args:
        func: The endpoint function to be protected.

    Returns:
        function: The decorated function that performs JWT verification.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401

        token = token.split(' ')[1]  # Extract the token from 'Bearer <token>'
        decoded_token = decode_jwt(token)

        if decoded_token:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Invalid token'}), 401

    return decorated_function


@app.route('/login', methods=['POST'])
def login():
    """
    Handles user login requests and generates JWT tokens on successful
    authentication.

    Returns:
        JSON: A response containing the JWT token or an error message
            if authentication fails.
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    role = authenticate(username, password)

    if role:
        token = generate_jwt(username, role)
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Endpoints
@app.route('/characters', methods=['GET'])
@protect_endpoint
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
@protect_endpoint
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
@protect_endpoint
def create_character():
    """
    Creates a new character.

    Request Body:
        A JSON object containing the following fields:
        - `name` (str, required): The name of the character.
        - `animal` (str, optional): The animal associated
        with the character.
        - `symbol` (str, optional): The symbol of the character.
        - `nickname` (str, optional): The nickname of the character.
        - `role` (str, optional): The role of the character.
        - `age` (int, required): The age of the character.
        - `death` (int, optional): The year of the character's death.
        - `house` (int, required): The ID of the house the character belongs to.
        - `strength` (int, required): The ID of the strength
        associated with the character.

    Returns:
        - 201 Created: If the character is created successfully.
        - 400 Bad Request: If the request body is invalid
        or missing required fields.
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
@protect_endpoint
def update_character(id):
    """
    Updates an existing character.

    Args:
        id (int): The ID of the character to update.

    Returns:
        JSON response:
            - 200 OK: If the character is updated successfully.
            - 400 Bad Request: If the request data is invalid
            or missing required fields.
            - 404 Not Found: If the character with the given ID is not found.
            - 500 Internal Server Error: If an unexpected
            error occurs during the update process.
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
@protect_endpoint
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
@protect_endpoint
def add_character_house():
    """
    Adds a new house to the database.

    **Request Body:**
        A JSON object containing the following field:
            - `name` (str, required): The name of the house.

    **Returns:**
        - 201 Created: If the house is created successfully.
        - 400 Bad Request: If the 'name' field is missing
        or unexpected error while adding to db.
    """
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': f'Missing field: {'name'}'}), 400
    new_house = service.add_house(data)
    if new_house:
        return jsonify(new_house), 201
    return jsonify(new_house), 400


@app.route('/characters/strength', methods=['POST'])
@protect_endpoint
def add_character_strength():
    """
    Adds a new strength to the database.

    **Request Body:**
        A JSON object containing the following field:
        - `name` (str, required): The name of the strength.

    **Returns:**
        - 201 Created: If the strength is created successfully.
        - 400 Bad Request: If the 'name' field is missing
        or unexpected error while adding to db.
    """
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': f'Missing field: {'name'}'}), 400
    new_strength = service.add_strength(data)
    if new_strength:
        return jsonify(new_strength), 201
    return jsonify(new_strength), 400


if __name__ == '__main__':
    app.run(debug=True)