import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@host:5432/polinavasiuk'
    SQLALCHEMY_TRACK_MODIFICATIONS = False