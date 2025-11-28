from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from BUDONG.api.core.database import get_db
from BUDONG.api.models.models import (
    TBjdTable,
    TJcgBjdTable,
    TCrimeCCTV,
    TPublicTransportByAdminDong,
    TNoise,
)

from BUDONG.api.schemas.schema_region import (
    RegionStatsResponse,
    RegionStatsItem,
    RegionInfo
)

router = APIRouter()


@router.get("/stats", response_model=RegionStatsResponse)
def get_region_stats(
    bjd_code: int = Query(..., description="법정동 코드"),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------------
    # 1. 기본 지역정보: 법정동명
    # -----------------------------------------------------------
    bjd = (
        db.query(TBjdTable)
        .filter(TBjdTable.bjd_code == bjd_code)
        .first()
    )

    if bjd is None:
        raise HTTPException(status_code=404, detail="해당 법정동을 찾을 수 없습니다.")

    # -----------------------------------------------------------
    # 2. 자치구명 조회 (범죄 통계용)
    # -----------------------------------------------------------
    jcg = (
        db.query(TJcgBjdTable)
        .filter(TJcgBjdTable.bjd_code == bjd_code)
        .first()
    )

    region_name = jcg.region_name_full if jcg else None

    # -----------------------------------------------------------
    # 3. 범죄/CCTV 통계 (자치구 단위)
    # -----------------------------------------------------------
    crime = None
    if region_name:
        crime = (
            db.query(TCrimeCCTV)
            .filter(TCrimeCCTV.jcg_name == region_name)
            .first()
        )

    # -----------------------------------------------------------
    # 4. 행정동 기반 대중교통 복잡도
    #    → 법정동코드 뒤 2자리 00으로 변환
    # -----------------------------------------------------------
    hjd_id = (bjd_code // 100) * 100

    transport = (
        db.query(TPublicTransportByAdminDong)
        .filter(TPublicTransportByAdminDong.hjd_id == hjd_id)
        .first()
    )

    # -----------------------------------------------------------
    # 5. 소음 데이터
    #    → 해당 지역 주변 소음 지점 중 가장 가까운 것 1개
    # -----------------------------------------------------------
    noise = None
    all_noise = db.query(TNoise).all()

    # 법정동 중심 추정 → TBjdTable에는 좌표 없음
    # 따라서 noise는 "정확한 주소 매칭" or "데이터 전체 중 임의 선택"
    # 여기서는 동일 지역주소 기반 매칭 시도
    if bjd.bjd_name:
        noise = (
            db.query(TNoise)
            .filter(TNoise.address.contains(bjd.bjd_name))
            .first()
        )

    # -----------------------------------------------------------
    # 6. RegionStatsItem 생성
    # -----------------------------------------------------------
    stats = RegionStatsItem(
        category="region",
        crime_num=crime.crime_num if crime else None,
        cctv_num=crime.cctv_num if crime else None,
        dangerous_rating=crime.dangerous_rating if crime else None,
        cctv_security_rating=crime.CCTV_security_rating if crime else None,
        passenger_num=transport.passenger_num if transport else None,
        complexity_rating=transport.complexity_rating if transport else None,
        noise_max=noise.noise_max if noise else None,
        noise_avg=noise.noise_avg if noise else None,
        noise_min=noise.noise_min if noise else None
    )

    region_info = RegionInfo(
        bjd_code=bjd_code,
        region_name_full=region_name
    )

    return RegionStatsResponse(
        region_stats=stats,
        region=region_info
    )
