from pydantic import BaseModel, Field
from typing import Optional

class InfrastructureCategoryRequest(BaseModel):
    category: str = Field(..., description="인프라 카테고리")
    latitude: float = Field(..., description="중심 위도")
    longitude: float = Field(..., description="중심 경도")
    radius_meters: int = Field(..., description="검색 반경 (미터)")


class InfrastructureItem(BaseModel):
    infra_id: str
    infra_category: str
    name: str
    address: Optional[str]
    latitude: float
    longitude: float


class InfrastructureResponse(BaseModel):
    infrastructure: list[InfrastructureItem]
