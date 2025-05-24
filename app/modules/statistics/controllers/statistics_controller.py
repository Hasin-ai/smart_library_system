from typing import List
from sqlalchemy.orm import Session
from app.modules.statistics.services.statistics_service import StatisticsService
from app.modules.statistics.schemas.responses import PopularBookResponse, ActiveUserResponse, SystemOverviewResponse

class StatisticsController:
    def __init__(self, db: Session):
        self.svc = StatisticsService(db)

    def get_popular(self, limit: int) -> List[PopularBookResponse]:
        return self.svc.popular_books(limit)

    def get_active(self, limit: int) -> List[ActiveUserResponse]:
        return self.svc.active_users(limit)

    def get_overview(self) -> SystemOverviewResponse:
        return self.svc.overview()
