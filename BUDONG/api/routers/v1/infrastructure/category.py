from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from BUDONG.api.core.database import get_db
from BUDONG.api.exception.global_exception_handler import APIError
from BUDONG.api.models.models import (
    TSchool,
    TPark,
    TStation,
)
from BUDONG.api.schemas.schema_infrastructure import (
    InfrastructureCategoryRequest,
    InfrastructureItem,
    InfrastructureResponse,
)
from BUDONG.util.geoutil import haversine

router = APIRouter()

VALID_CATEGORIES = {
    "school",
    "park",
    "subway_station",   # subway + train 포함 가능
}


@router.post("/category", response_model=InfrastructureResponse)
def search_infrastructure_by_category(
    payload: InfrastructureCategoryRequest,
    db: Session = Depends(get_db)
):
    category = payload.category
    lat = payload.latitude
    lon = payload.longitude
    radius = payload.radius_meters

    if category not in VALID_CATEGORIES:
        raise APIError(
            code="INVALID_CATEGORY",
            message=f"'{category}'는 지원하지 않는 카테고리입니다.",
            status_code=400,
        )

    result = []

    # ------------------------------------------------
    # SCHOOL
    # ------------------------------------------------
    if category == "school":
        items = db.query(TSchool).all()
        for s in items:
            if s is None:
                continue
            if s.lat is None or s.lon is None:
                continue
            dist = haversine(lat, lon, s.lat, s.lon)
            if dist <= radius:
                result.append(
                    InfrastructureItem(
                        infra_id=str(s.school_id),
                        infra_category="school",
                        name=s.school_name,
                        address=s.address,
                        latitude=s.lat,
                        longitude=s.lon,
                    )
                )

    # ------------------------------------------------
    # PARK
    # ------------------------------------------------
    elif category == "park":
        items = db.query(TPark).all()
        for p in items:
            if p.lat is None or p.lon is None:
                continue
            dist = haversine(lat, lon, p.lat, p.lon)
            if dist <= radius:
                result.append(
                    InfrastructureItem(
                        infra_id=p.park_name,
                        infra_category="park",
                        name=p.park_name,
                        address=p.address,
                        latitude=p.lat,
                        longitude=p.lon,
                    )
                )

    # ------------------------------------------------
    # STATION (지하철역)
    # ------------------------------------------------
    elif category == "subway_station":
        items = db.query(TStation).all()
        for st in items:
            if st.lat is None or st.lon is None:
                continue
            dist = haversine(lat, lon, st.lat, st.lon)
            if dist <= radius:
                result.append(
                    InfrastructureItem(
                        infra_id=str(st.station_id),
                        infra_category="subway_station",
                        name=st.station_name,
                        address=None,
                        latitude=st.lat,
                        longitude=st.lon,
                    )
                )

    return InfrastructureResponse(infrastructure=result)
