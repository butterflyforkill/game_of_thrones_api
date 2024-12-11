from sqlalchemy.orm import relationship
from database import db


class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    animal = db.Column(db.String(50), nullable=True, unique=False)
    symbol = db.Column(db.String(50), nullable=True, unique=False)
    nickname = db.Column(db.String(50), nullable=True, unique=False)
    role = db.Column(db.String(50), nullable=False, unique=False)
    age = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=True)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'), nullable=False)
    strength_id = db.Column(db.Integer, db.ForeignKey('strengthes.id'), nullable=False)
    house = relationship("House")
    strength = relationship("Strength")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "house": self.house.name,  # Access the house name
            "animal": self.animal,
            "symbol": self.symbol,
            "nickname": self.nickname,
            "role": self.role,
            "age": self.age,
            "death": self.death,
            "strength": self.strength.name,  # Access the strength name
        }


class House(db.Model):
    __tablename__ = 'houses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)


class Strength(db.Model):
    __tablename__ = 'strengthes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)