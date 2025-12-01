from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from BUDONG.api.core.database import get_db
from BUDONG.api.models.models import (
    TBuilding, TSchool, TStation, TPark
)
from BUDONG.api.schemas.schema_search import (
    SearchPointRequest,
    SearchPointResponse,
    SearchPointBuilding,
    SearchPointInfra
)
from BUDONG.util.geoutil import haversine

router = APIRouter()


@router.post("/point", response_model=SearchPointResponse)
def search_point(
    payload: SearchPointRequest,
    db: Session = Depends(get_db)
):

    lat = payload.latitude
    lon = payload.longitude
    radius = payload.radius_meters

    distance_expression = func.ST_Distance_Sphere(
        func.Point(TBuilding.lon, TBuilding.lat),  
        func.Point(lon, lat)
    )

    building_list = db.query(TBuilding).filter(distance_expression <= radius).all()

    result_buildings = [
        SearchPointBuilding(
            building_id=b.building_id,
            bjd_code=b.bjd_code,
            address=b.address,
            building_name=b.building_name,
            building_type=b.building_type,
            build_year=b.build_year,
            total_units=b.total_units,
            latitude=b.lat,
            longitude=b.lon
        )
        for b in building_list
    ]

    # ================================
    # 2. 인프라 조회 (학교 + 역 + 공원)
    # ================================

    # --- 학교 ---

    distance_expression = func.ST_Distance_Sphere(
        func.Point(TSchool.lon, TSchool.lat),  
        func.Point(lon, lat)
    )

    school_list = db.query(TSchool).filter(distance_expression <= radius).all()
    school_result = [
        SearchPointInfra(
            type="school",
            name=s.school_name,
            address=s.address,
            latitude=s.lat,
            longitude=s.lon
        )
        for s in school_list
    ]

    # --- 지하철역 ---
    distance_expression = func.ST_Distance_Sphere(
        func.Point(TStation.lon, TStation.lat),  
        func.Point(lon, lat)
    )

    station_list = db.query(TStation).filter(distance_expression <= radius).all()
    station_result = [
        SearchPointInfra(
                    type="subway_station",
                    name=st.station_name,
                    address=None,
                    latitude=st.lat,
                    longitude=st.lon
        )
        for st in station_list
    ]

    distance_expression = func.ST_Distance_Sphere(
        func.Point(TPark.lon, TPark.lat),  
        func.Point(lon, lat)
    )

    # park
    park_list = db.query(TPark).filter(distance_expression <= radius).all()
    park_result = [
        SearchPointInfra(
            type="park",
            name=p.park_name,
            address=p.address,
            latitude=p.lat,
            longitude=p.lon
        )
        for p in park_list
    ]
    

    infra_results = school_result + park_result + station_result
    return SearchPointResponse(
        buildings=result_buildings,
        infrastructure=infra_results,
        search_radius=radius,
        result_count=len(result_buildings) + len(infra_results)
    )
