from sqlalchemy.sql import func
from database import db


class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    animal = db.Column(db.String(50), nullable=True, unique=True)
    symbol = db.Column(db.String(50), nullable=False, unique=True)
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False, unique=False)
    age = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    strength_id = db.Column(db.Integer, db.ForeignKey('strengthes.id'), nullable=False)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class House(db.Model):
    __tablename__ = 'houses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Strength(db.Model):
    __tablename__ = 'strengthes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)