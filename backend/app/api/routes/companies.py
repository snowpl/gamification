import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import CompanyRead, CompanyCreate

router = APIRouter(prefix="/company", tags=["companies"])


@router.get("/", response_model=CompanyRead)
def read_company(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve company.
    """
    company = session.get(CompanyRead, current_user.company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not current_user.is_superuser and (company.id != current_user.company_id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return company
