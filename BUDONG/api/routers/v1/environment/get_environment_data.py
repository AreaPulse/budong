from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from BUDONG.api.core.database import get_db
from BUDONG.api.models.models import TNoise
from BUDONG.api.schemas.schema_environment import (
    EnvironmentDataItem,
    EnvironmentDataResponse,
)

from BUDONG.util.geoutil import haversine

router = APIRouter()


@router.get("/data", response_model=EnvironmentDataResponse)
def get_environment_data(
    latitude: float = Query(..., description="위도"),
    longitude: float = Query(..., description="경도"),
    db: Session = Depends(get_db),
):
    # 모든 noise 지점 조회
    noise_list = db.query(TNoise).all()
    if not noise_list:
        raise HTTPException(status_code=404, detail="환경 데이터가 없습니다.")

    nearest_noise = None
    min_dist = float("inf")

    for n in noise_list:
        if n is None:
            continue
        if n.lat is None or n.lon is None:
            continue

        dist = haversine(latitude, longitude, n.lat, n.lon)
        if dist < min_dist:
            min_dist = dist
            nearest_noise = n

    if nearest_noise is None:
        raise HTTPException(status_code=404, detail="가까운 소음 지점을 찾을 수 없습니다.")

    item = EnvironmentDataItem(
        address=nearest_noise.address,
        noise_max=nearest_noise.noise_max,
        noise_avg=nearest_noise.noise_avg,
        noise_min=nearest_noise.noise_min,
        latitude=nearest_noise.lat,
        longitude=nearest_noise.lon,
    )

    return EnvironmentDataResponse(
        environment_data=[item],
        latitude=latitude,
        longitude=longitude,
    )
