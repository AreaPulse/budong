from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EnvironmentDataItem(BaseModel):
    address: Optional[str]
    noise_max: Optional[int]
    noise_avg: Optional[int]
    noise_min: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]


class EnvironmentDataResponse(BaseModel):
    environment_data: List[EnvironmentDataItem]
    latitude: float
    longitude: float