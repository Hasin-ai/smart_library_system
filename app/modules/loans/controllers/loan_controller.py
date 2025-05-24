from typing import List
from sqlalchemy.orm import Session
from app.modules.loans.services.loan_service import LoanService
from app.modules.loans.schemas.requests import LoanCreateRequest, LoanExtendRequest
from app.modules.loans.schemas.responses import LoanResponse

class LoanController:
    def __init__(self, db: Session):
        self.svc = LoanService(db)

    def create(self, data: LoanCreateRequest) -> LoanResponse:
        l = self.svc.create_loan(data)
        return LoanResponse.model_validate(l)

    def return_(self, loan_id: int) -> LoanResponse:
        l = self.svc.return_loan(loan_id)
        return LoanResponse.model_validate(l)

    def extend(self, loan_id: int, data: LoanExtendRequest) -> LoanResponse:
        l = self.svc.extend_loan(loan_id, data)
        return LoanResponse.model_validate(l)

    def list_overdue(self) -> List[LoanResponse]:
        loans = self.svc.get_overdue()
        return [LoanResponse.model_validate(l) for l in loans]
