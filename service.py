from database import db
from sqlalchemy import update, or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Character, House, Strength


def house_strength_filters(filters):
    """
    Filters a SQLAlchemy query for characters based on
    provided filters for house and strength.

    Args:
        filters (list): A list of dictionaries containing filtering criteria.
            Each dictionary should have a key and a value.
            Supported keys:
                - 'house': Filter characters by house name (ilike match).
                - 'strength': Filter characters by strength name (ilike match).

    Returns:
        SQLAlchemy.orm.query.Query: The filtered query object.
    """
    query = Character.query

    for filter_dict in filters:
        for key, value in filter_dict.items():
            if key == 'house':
                query = query.join(
                    House, Character.house_id == House.id).filter(House.name.ilike(f"{value}%"))
            elif key == 'strength':
                query = query.join(
                    Strength, Character.strength_id == Strength.id).filter(Strength.name.ilike(f"{value}%"))
    return query


def other_filters(query, filters):
    """
    Filters a SQLAlchemy query for characters based on
    provided filters excluding house and strength.

    Args:
        query (SQLAlchemy.orm.query.Query): The base query object to filter.
        filters (list): A list of dictionaries containing filtering criteria.
            Each dictionary should have a key and a value.

    Returns:
        SQLAlchemy.orm.query.Query: The filtered query object.
    """
    conditions = []
    for filter in filters:
        for key in filter.keys():
            if key == 'age':
                # Handle filtering for integer 'age' column
                conditions.append(Character.age == filter[key])
            elif key == 'house':
                conditions.append(Character.house.has(House.name.ilike(f"%{filter[key]}%")))
            elif key == 'strength':
                conditions.append(Character.strength.has(Strength.name.ilike(f"%{filter[key]}%")))
            elif key != 'house' and key != 'strength':
                try:
                    # Attempt to access the attribute and create a filter condition
                    conditions.append(getattr(Character, key).ilike(f"%{filter[key]}%"))
                except AttributeError:
                    # Handle the case where the attribute doesn't exist
                    print(f"Warning: Invalid filter key '{key}'") 
    if conditions:
        query = query.filter(or_(*conditions))
    return query


def characters_sort(unsorted_characters, sort_order, sort_by):
    """
    Sorts a list of character objects based on the specified sort criteria.

    Args:
        unsorted_characters (list): A list of Character objects.
        sort_order (str): The order of sorting (asc or desc).
        sort_by (str): The attribute to sort by (a valid Character model attribute).

    Returns:
        list: The sorted list of Character objects.
    """
    if sort_order == 'asc':
        sort_function = getattr(Character, sort_by).asc()
    else:
        sort_function = getattr(Character, sort_by).desc()
    return unsorted_characters.order_by(sort_function)


def get_character(id):
    """
    Retrieves a character by its ID from the database.

    Args:
        id (int): The unique ID of the character.

    Returns:
        dict | None: A dictionary representation of the character object if found, 
                      None otherwise.
    """
    character = Character.query.get(id)
    if character:
        return character.to_dict()
    return None


def create_character(data_character):
    """
    Creates a new character object and saves it to the database.

    Args:
        data_character (dict): A dictionary containing character data.
            Required keys:
                - name (str)
                - animal (str)
                - symbol (str)
                - nickname (str)
                - role (str)
                - age (int)
                - house (int): ID of the associated house.
                - strength (int): ID of the associated strength.
            Optional keys:
                - death (int): Year of death (if applicable).

    Returns:
        dict: A dictionary representation of the newly created character object
              or a dictionary containing an error message if creation fails.
    """
    # Create a new Character object
    character = Character(
        name=data_character['name'],
        animal=data_character['animal'],
        symbol=data_character['symbol'],
        nickname=data_character['nickname'],
        role=data_character['role'],
        age=data_character['age'],
        death=data_character.get('death', None),
        house_id=data_character['house'],
        strength_id=data_character['strength'],
    )
    db.session.add(character)

    try:
        db.session.commit()
    except Exception as e:
        # Rollback in case of errors
        db.session.rollback()
        return {'error': f'Failed to create character: {str(e)}'}

    return character.to_dict()


def update_character(update_data_character, character_id):
    """
    Updates a character object in the database with provided data.

    Args:
        update_data_character (dict): A dictionary containing updated character data.
            Keys should correspond to valid Character model attributes.
        character_id (int): The unique ID of the character to update.

    Returns:
        dict: A dictionary containing a success message if the update is successful,
              or an error message if the update fails.
    """
    try:
        # Update character fields with validated data
        stmt = (
            update(Character)
            .where(Character.id == character_id)
            .values(**update_data_character.dict())
        )
        db.session.execute(stmt)
        db.session.commit()
        return {'message': 'Character updated successfully'}
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of error
        return {'problem4=error': str(e)}


def delete_character(id):
    """
    Deletes a character object from the database by its ID.

    Args:
        id (int): The unique ID of the character to delete.

    Returns:
        dict: A dictionary containing a success message if the deletion is successful,
              or an error message if the deletion fails.
    """
    try:
        delete_character = Character.query.get(id)
        db.session.delete(delete_character)
        db.session.commit()
        return {'message': 'Character deleted successfully'}
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of error
        return {'error': str(e)}


def add_house(house_data):
    new_house = House(name=house_data['name'])
    db.session.add(new_house)

    try:
        db.session.commit()
        return {'message': 'House created successfully'}
    except SQLAlchemyError as e:
        db.session.rollback()
        if isinstance(e, IntegrityError) and 'duplicate key value violates unique constraint' in str(e):
            return {'error': f'House with name "{house_data["name"]}" already exists.'}
        else:
            return {'error': f'Database error: {str(e)}'}
    except Exception as e:
        db.session.rollback()
        return {'error': f'Unexpected error: {str(e)}'}


def add_strength(strength_data):
    new_house = Strength(name=strength_data['name'])
    db.session.add(new_house)

    try:
        db.session.commit()
        return {'message': 'Strength created successfully'}
    except SQLAlchemyError as e:
        db.session.rollback()
        if isinstance(e, IntegrityError) and 'duplicate key value violates unique constraint' in str(e):
            return {'error': f'House with name "{strength_data["name"]}" already exists.'}
        else:
            return {'error': f'Database error: {str(e)}'}
    except Exception as e:
        db.session.rollback()
        return {'error': f'Unexpected error: {str(e)}'}