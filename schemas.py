from pydantic import BaseModel, ValidationError


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