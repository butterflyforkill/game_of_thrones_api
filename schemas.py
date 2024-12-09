from pydantic import BaseModel, ValidationError


class CharacterUpdate(BaseModel):
    name: str
    animal: str
    symbol: str | None = None  # Optional fields
    nickname: str
    role: str
    age: int
    death: int | None = None
    house_id: int
    strength_id: int