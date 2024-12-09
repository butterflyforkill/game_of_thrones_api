from database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update
from models import Character, House, Strength 
from schemas import CharacterUpdate


def characters_filter(filters):
    query = Character.query
    for key, value in filters:
        if key == 'house':
            query = query.join(House).filter(House.name.ilike(f"%{value}%"))
        elif key == 'strength':
            query = query.join(Strength).filter(Strength.name.ilike(f"%{value}%"))
        else:
            query = query.filter(Character.name.ilike(f"%{value}%"))
    
    return query

def characters_sort(unsorted_characters, sort_order, sort_by):
    if sort_order:
        return unsorted_characters.order_by(getattr(Character, sort_by).desc())
    else:
        return unsorted_characters.order_by(getattr(Character, sort_by))


def get_character(id):
    character = Character.query.get(id)
    if character:
        return character.to_dict()
    return None


def create_character(data_character):
     # Create a new Character object
    character = Character(
        name=data_character['name'],
        animal=data_character['animal'],
        symbol=data_character['symbol'],
        nickname=data_character['nickname'],
        role=data_character['role'],
        age=data_character['age'],
        death=data_character.get('death', None),  # Handle optional death field
        house_id=data_character['house'],
        strength_id=data_character['strength'],
    )
    # Add the character to the database session
    db.session.add(character)

    try:
        # Commit the changes to the database
        db.session.commit()
    except Exception as e:
        # Rollback in case of errors
        db.session.rollback()
        return {'error': f'Failed to create character: {str(e)}'}

    # Return the newly created character data
    return character.to_dict()


def update_character(update_data_character, character_id):
    # Update character fields with validated data
    try:
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