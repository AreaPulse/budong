from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from BUDONG.api.core.database import get_db
from BUDONG.api.models import TUserSavedBuilding
from BUDONG.api.schemas.schema_saved_buildings import SavedBuildingsResponse

router = APIRouter()

@router.get("/saved-buildings", response_model=SavedBuildingsResponse)
def get_saved_buildings(user_id: int, db: Session = Depends(get_db)):
    saved_buildings = (
        db.query(TUserSavedBuilding)
        .options(joinedload(TUserSavedBuilding.building))  # 🔥 JOIN building table
        .filter(TUserSavedBuilding.user_id == user_id)
        .all()
    )

    return {
        "saved_buildings": saved_buildings,
        "total_count": len(saved_buildings)
    }
