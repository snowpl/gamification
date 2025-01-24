from sqlmodel import Session, create_engine, select
from sqlmodel import SQLModel
from app import crud
from app.core.config import settings
from app.models import Company, CompanyCreate, Department, DepartmentCreate, Skill, SkillCreate, User, UserCreate
from app.core.data_provider import create_marketing_department, create_sales_department
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    company = session.exec(
        select(Company).where(Company.name == "Staff Bit")
    ).first()
    if not company:
        company_in = CompanyCreate(
            name="Staff Bit"
        )
        company = crud.create_company(session=session, company_in=company_in)
    
    logger.info("Looking for department")
    department = session.exec(
        select(Department).where(Department.company_id == company.id)
    ).first()
    if not department:
        logger.info("No department found")
        marketing = create_marketing_department(session=session, company_id=company.id)
        logger.info(marketing)

        delivery_department = DepartmentCreate(
            name="Delivery",
            company_id=company.id
        )
        department = crud.create_department(session=session, department_in=delivery_department)

        hr_department = DepartmentCreate(
            name="HR",
            company_id=company.id
        )
        department = crud.create_department(session=session, department_in=hr_department)
        
        admin_department = DepartmentCreate(
            name="Administration",
            company_id=company.id
        )
        department = crud.create_department(session=session, department_in=admin_department)
        
        cs_department = DepartmentCreate(
            name="Customer Service",
            company_id=company.id
        )
        department = crud.create_department(session=session, department_in=cs_department)

        sales = create_sales_department(session=session, company_id=company.id)
        logger.info(sales)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
           is_superuser=True,
            company_id=company.id,
            department_id=department.id,
            current_xp=0,
            full_name="Admin Test"
        )
        user = crud.create_user(session=session, user_create=user_in)
