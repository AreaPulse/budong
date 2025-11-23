from fastapi import APIRouter
from BUDONG.api.routers.v1.buildings import detail

router = APIRouter()

# 각 라우터 등록
router.include_router(detail.router, tags=["buildings"])
