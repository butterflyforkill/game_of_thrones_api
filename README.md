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
    - Parameters: 
        - `sort_by` (optional): Field to sort by.
        - `sort_order` (optional): 'asc' or 'desc'.
        - `limit` (optional, default=20): Number of characters to return.
        - `skip` (optional, default=0): Number of characters to skip for pagination.
        - Additional query parameters for filtering.
- **GET** ```/characters/{id}```
    - Response: JSON representation of the character.
- **POST** ```/characters```
    - Body: JSON with character details (refer to function docstring for required fields).
- **PUT** ```/characters/{id}```
    - Body: JSON with updated character details.
- **DELETE** ```/characters/{id}```
    - Response: JSON message confirming deletion.

**House and Strength**
- **POST** `/characters/house`
    - Body: JSON with name for the house.
- **POST** `/characters/strength`
    - Body: JSON with name for the strength.

**Error Handling**
- 400 Bad Request: For missing or invalid data.
- 404 Not Found: When trying to access non-existent resources.
- 500 Internal Server Error: For unexpected errors.