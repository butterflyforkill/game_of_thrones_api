from .database import db
from sqlalchemy.exc import SQLAlchemyError
from .models import Character, House, Strength 


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