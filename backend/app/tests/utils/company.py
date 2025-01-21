from sqlmodel import Session

from app import crud
from app.models import Company, CompanyCreate
from app.tests.utils.utils import random_lower_string

def create_random_company(db: Session) -> Company:
    title = random_lower_string()
    company_in = CompanyCreate(name=title)
    return crud.create_company(session=db, company_in=company_in)
