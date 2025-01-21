import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.company import create_random_company

def test_read_company(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    company = create_random_company(db)
    response = client.get(
        f"{settings.API_V1_STR}/company",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == company.name
    assert content["level"] == company.level
    assert content["current_xp"] == company.current_xp

def test_read_company_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/company",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Company not found"

def test_read_company_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    company = create_random_company(db)
    response = client.get(
        f"{settings.API_V1_STR}/company",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
