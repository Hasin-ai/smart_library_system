from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.statistics.controllers.statistics_controller import StatisticsController
from app.modules.statistics.schemas.responses import PopularBookResponse, ActiveUserResponse, SystemOverviewResponse

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/overview", response_model=SystemOverviewResponse)
async def overview(db: Session = Depends(get_db)):
    return StatisticsController(db).get_overview()

@router.get("/popular-books", response_model=List[PopularBookResponse])
async def popular(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    return StatisticsController(db).get_popular(limit)

@router.get("/active-users", response_model=List[ActiveUserResponse])
async def active(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    return StatisticsController(db).get_active(limit)
