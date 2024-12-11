from pydantic import BaseModel, Field, field_validator
import re


class CharacterUpdate(BaseModel):
    name: str
    animal: str | None = None
    symbol: str | None = None
    nickname: str | None = None
    role: str
    age: int
    death: int | None = None
    house_id: int
    strength_id: int
    
    @field_validator(
        'name',
        'animal',
        'symbol',
        'nickname',
        'role'
        )
    @classmethod
    def validate_name(cls, v):
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError(f'{v} must only contain letters and spaces.')
        return v
    
    @field_validator(
        'name',
        'animal',
        'symbol',
        'nickname',
        'role'
        )
    @classmethod
    def validate_name_length(cls, v):
        if len(v) < 3:
            raise ValueError(f'{v} must be at least 3 characters long.')
        return v


class CharacterCreate(BaseModel):
    name: str = Field(..., max_length=50)
    animal: str = Field(None, max_length=50)
    symbol: str = Field(None, max_length=50)
    nickname: str = Field(None, max_length=50)
    role: str = Field(None, max_length=50)
    age: int = Field(...)
    death: int = None
    house: int = Field(...)
    strength: int = Field(...)
    
    @field_validator(
        'name',
        'animal',
        'symbol',
        'nickname',
        'role'
        )
    @classmethod
    def validate_name(cls, v):
        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError(f'{v} must only contain letters and spaces.')
        return v
    
    @field_validator(
        'name',
        'animal',
        'symbol',
        'nickname',
        'role'
        )
    @classmethod
    def validate_name_length(cls, v):
        if len(v) < 3:
            raise ValueError(f'{v} must be at least 3 characters long.')
        return v