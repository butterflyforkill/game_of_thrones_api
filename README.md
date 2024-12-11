# game_of_thrones_api: Character Management API


A Flask-based RESTful API for managing characters in a fictional or game universe.

## Features

- **CRUD Operations for Characters**:
  - **GET /characters**: Retrieve characters with pagination and filtering options.
  - **GET /characters/{id}**: Fetch a specific character by ID.
  - **POST /characters**: Add a new character.
  - **PUT /characters/{id}**: Update character data.
  - **DELETE /characters/{id}**: Remove a character.

- **House and Strength Management**:
  - **POST /characters/house**: Add a new house for characters.
  - **POST /characters/strength**: Add a new strength attribute for characters.


## Setup

### Prerequisites

- Python 3.8+
- Flask
- SQLAlchemy
- Pydantic (for data validation)
- Any necessary database (e.g., PostgreSQL, SQLite)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/butterflyforkill/game_of_thrones_api.git
   cd game_of_thrones_api
   ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the environment:**
    - Adjust the SQLALCHEMY_DATABASE_URI in your Config class or via environment variables for different deployment environments.

5. **Initialize the database:**
    ```bash
    python -m flask db init
    python -m flask db migrate
    python -m flask db upgrade
    ```

### Running the Application

To run the application in development mode:
```bash
flask run
```
Or if you're running directly from the script:
```bash
python app.py
```

### API Endpoints 
**Characters** 
- **GET** ```/characters```
    - **Purpose**: Retrieve a list of characters with pagination and filtering options.
    - **Parameters**: 
        - `sort_by` (optional): Field to sort by.
        - `sort_order` (optional): 'asc' or 'desc'.
        - `limit` (optional, default=20): Number of characters to return.
        - `skip` (optional, default=0): Number of characters to skip for pagination.
        - Additional query parameters for filtering.
    - **Example Use**:
      ```bash
      GET /characters?sort_by=name&sort_order=asc&limit=10&skip=0&house=Stark
      ```
- **GET** ```/characters/{id}```
    - **Purpose**: Retrieve details of a specific character by its ID.
    - **Parameters**:
        - `id` (path parameter): The ID of the character.
    - **Example Use**:
      ```bash
      GET /characters/1
      ```
- **POST** ```/characters```
    - **Purpose**: Create a new character entry.
    - **Body**: JSON containing character details (e.g., name, house, animal, etc.).
    - **Example Use**:
      ```bash
      POST /characters
        {
        "name": "Jon Snow",
        "house": "Stark",
        "animal": "Direwolf",
        "symbol": "Ice",
        "nickname": "The Bastard",
        "role": "Knight",
        "age": 24,
        "death": null,
        "strength": "StrengthID1"
        }
      ```
- **PUT** ```/characters/{id}```
    - **Purpose**: Update an existing character's details.
    - **Parameters**:
        - `id` (path parameter): The ID of the character to update.
    - **Body**: JSON with updated character details.
    - **Example Use**:
      ```bash
      PUT /characters/1
      {
        "name": "Jon Snow",
        "age": 25
      }
      ```
- **DELETE** ```/characters/{id}```
    - **Purpose**: Delete a character by ID.
    - **Parameters**:
        - id (path parameter): The ID of the character to delete.
    - **Response**: JSON message confirming deletion.
    - **Example Use**:
      ```bash
      DELETE /characters/1
      ```

**House and Strength**
- **POST** `/characters/house`
    - **Purpose**: Add a new house for characters.
    - **Body**: JSON with name for the house.
    - **Example Use**:
      ```bash
      POST /characters/house
      {
        "name": "Targaryen"
      }   
      ```
- **POST** `/characters/strength`
    - **Purpose**: Add a new strength attribute for characters.
    - **Body**: JSON with name for the house.
    - **Example Use**:
      ```bash
      POST /characters/strength
      {
        "name": "Bravery"
      }   
      ```
**Notes on Usage**:
- When making these requests, ensure you are using the correct HTTP method (GET, POST, PUT, DELETE).
- For POST and PUT requests, the body should be in JSON format, and content type headers should be set accordingly (Content-Type: application/json).
Error responses could include 400 for bad requests (invalid data), 404 for not found resources, and 500 for internal server errors.
- Authentication or authorization headers might be required in a production environment, which aren't shown here but should be considered for security.

**Error Handling**
- 400 Bad Request: For missing or invalid data.
- 404 Not Found: When trying to access non-existent resources.
- 500 Internal Server Error: For unexpected errors.