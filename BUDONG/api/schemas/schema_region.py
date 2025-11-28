from pydantic import BaseModel
from typing import List, Optional


class RegionStatsItem(BaseModel):
    category: str                   # crime / cctv / transport / noise
    crime_num: Optional[int]
    cctv_num: Optional[int]
    dangerous_rating: Optional[int]
    cctv_security_rating: Optional[int]
    passenger_num: Optional[int]
    complexity_rating: Optional[int]
    noise_max: Optional[int]
    noise_avg: Optional[int]
    noise_min: Optional[int]


class RegionInfo(BaseModel):
    bjd_code: int
    region_name_full: Optional[str]   # 자치구명


class RegionStatsResponse(BaseModel):
    region_stats: RegionStatsItem
    region: RegionInfo
