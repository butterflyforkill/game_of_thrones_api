import random
from flask import Flask, request, jsonify, abort
import json_parcer


app = Flask(__name__)

characters = json_parcer.load_data('data.json')

@app.route('/characters', methods=['GET'])
def get_characters():
    """
    Fetch all characters (with Pagination)
    
    """
    name = request.args.get('name')
    house = request.args.get('house')
    role = request.args.get('role')
    age_more_than = request.args.get('age_more_than')
    age_less_than = request.args.get('age_less_than')
    limit = int(request.args.get('limit', 20))
    skip = int(request.args.get('offset', 0))

    filtered_characters = [char for char in characters if
                       (not name or char['name'].lower() == name.lower()) and
                       (not house or str(char['house']).lower().find(house.lower()) >= 0) and
                       (not role or char['role'].lower() == role.lower()) and
                       (not age_more_than or char['age'] >= int(age_more_than)) and
                       (not age_less_than or char['age'] <= int(age_less_than))]


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
    Fetch a specific character by ID
    """
    for character in characters:
        if character['id'] == id:
            return jsonify(character)
    abort(404, description="Character not found")


if __name__ == '__main__':
    app.run(debug=True)