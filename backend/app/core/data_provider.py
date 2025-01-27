import uuid
from requests import Session
from app import crud
from app.models import AvailableTaskCreate, DepartmentCreate, EmployeeTask
from app.api.users.skills_models import GlobalSkillCreate

def create_sales_department(session:Session, company_id:uuid) -> EmployeeTask:
    sales_department = DepartmentCreate(
        name="Sales",
        company_id=company_id
    )
    department = crud.create_department(session=session, department_in=sales_department)

    content_skills = GlobalSkillCreate(
        name="Sales Skill",
        department_id=department.id,
        xp=0,
        level=0,
        description="Everything related to sales skill #1"
    )
    cs = crud.create_global_skill(session=session, skill_in=content_skills)

    task1 = AvailableTaskCreate(
        title="Research client needs",
        description="Research what the client needs",
        requires_approval=False,
        department_id=department.id,
        skill_id=cs.id,
        approved=False,
        department_xp=200,
        skill_xp=100,
        company_xp=200,
        person_xp= 100,
        company_id=department.company_id)
    
    taks = crud.create_available_task(session=session, task_in=task1)
        

def create_marketing_department(session: Session, company_id: uuid) -> EmployeeTask:
    marketing_department = DepartmentCreate(
            name="Marketing",
            company_id=company_id
    )
    marketing_department = crud.create_department(session=session, department_in=marketing_department)
        
    content_skills = GlobalSkillCreate(
        name="Content Creation",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to content creation"
    )
    cs = crud.create_global_skill(session=session, skill_in=content_skills)

    research = GlobalSkillCreate(
        name="Research Creation",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to reaserch in marketing"
    )
    rs = crud.create_global_skill(session=session, skill_in=research)

    campaigns = GlobalSkillCreate(
        name="Campaigns",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to marketing campaigns"
    )
    camcs = crud.create_global_skill(session=session, skill_in=campaigns)

    partner = GlobalSkillCreate(
        name="Partnerships",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to partnerships"
    )
    pars = crud.create_global_skill(session=session, skill_in=partner)

    sm = GlobalSkillCreate(
        name="Social Media",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to social media"
    )
    sms = crud.create_global_skill(session=session, skill_in=sm)
    
    website = GlobalSkillCreate(
        name="Website",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to website"
    )
    ws = crud.create_global_skill(session=session, skill_in=website)

    analytics = GlobalSkillCreate(
        name="Analytics",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to analytics"
    )
    anas = crud.create_global_skill(session=session, skill_in=analytics)

    accountbased = GlobalSkillCreate(
        name="Account Based Marketing",
        department_id=marketing_department.id,
        xp=0,
        level=0,
        description="Everything related to account based marketing"
    )
    accs = crud.create_global_skill(session=session, skill_in=accountbased)

    task1 = AvailableTaskCreate(
        title="Research client needs",
        description="Research what the client needs",
        requires_approval=False,
        department_id=marketing_department.id,
        skill_id=rs.id,
        approved=False,
        department_xp=20,
        skill_xp=10,
        company_xp=2,
        person_xp= 1,
        company_id=marketing_department.company_id)
    
    taks = crud.create_available_task(session=session, task_in=task1)
    
    task2 = AvailableTaskCreate(
        title="Ads",
        description="Prepare ad campaign for internal use case",
        requires_approval=True,
        department_id=marketing_department.id,
        skill_id=camcs.id,
        approved=False,
        department_xp=20,
        skill_xp=10,
        company_xp=2,
        person_xp= 1,
        company_id=marketing_department.company_id)
    
    taks = crud.create_available_task(session=session, task_in=task1)
    return taks