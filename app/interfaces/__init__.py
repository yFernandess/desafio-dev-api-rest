from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field


class CustomBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    def as_json(self) -> dict:
        return jsonable_encoder(self)


class CustomTimableModel(CustomBaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
