from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BuildingRequest(BaseModel):
    building_id: int = Field(..., description="빌딩id")

# -------------------------
# Building 기본 정보
# -------------------------
class BuildingDetail(BaseModel):
    building_id: int
    bjd_code: str
    address: Optional[str]
    building_name: Optional[str]
    building_type: Optional[str]
    build_year: Optional[int]
    total_units: Optional[int]
    latitude: float
    longitude: float


# -------------------------
# 거래 정보
# -------------------------
class BuildingTransaction(BaseModel):
    tx_id: int
    building_id: int
    transaction_date: datetime
    price: int
    area_sqm: float
    floor: int


# -------------------------
# 리뷰 정보
# -------------------------
class BuildingReview(BaseModel):
    review_id: int
    user_id: int
    building_id: int
    rating: int
    content: str
    created_at: datetime


# -------------------------
# 주변 인프라 정보
# -------------------------
class NearbyInfrastructure(BaseModel):
    infra_id: int
    infra_category: str
    name: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float


# -------------------------
# 지역 통계
# -------------------------
class RegionStat(BaseModel):
    stats_id: int
    bjd_code: str
    stats_year: int
    stats_type: str
    stats_value: float


# -------------------------
# 환경 데이터
# -------------------------
class EnvironmentData(BaseModel):
    data_id: int
    station_id: int
    measurement_time: datetime
    pm10_value: int
    pm2_5_value: int
    noise_db: float


# -------------------------
# 최종 응답 구조
# -------------------------
class BuildingDetailResponse(BaseModel):
    building: BuildingDetail
    transactions: List[BuildingTransaction]
    reviews: List[BuildingReview]
    nearby_infrastructure: List[NearbyInfrastructure]
    region_stats: List[RegionStat]
    environment_data: List[EnvironmentData]
