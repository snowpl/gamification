from sqlmodel import Session

from app import crud
from app.models import CompanyCreate

def test_create_company(db: Session) -> None:
    company_in = CompanyCreate(name = "Test Company")
    company = crud.create_company(session=db, company_in=company_in)
    assert company.name == "Test Company"
    assert company.current_xp == 0
    assert company.level == 0