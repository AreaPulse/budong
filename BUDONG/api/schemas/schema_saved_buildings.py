from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Building(BaseModel):
    building_id: int
    address: str
    building_name: str
    building_type: str
    build_year: int
    total_units: int

    class Config:
        orm_mode = True

class SavedBuilding(BaseModel):
    save_id: int
    user_id: int
    building_id: int
    memo: str | None
    created_at: datetime
    building: Building | None  # 🔥 Include joined building data

    class Config:
        orm_mode = True

class SavedBuildingsResponse(BaseModel):
    saved_buildings: list[SavedBuilding]
    total_count: int