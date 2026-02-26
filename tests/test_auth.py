import pytest


@pytest.mark.asyncio
async def test_register(client):

    response = await client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"


@pytest.mark.asyncio
async def test_login(client):

    await client.post(
        "/auth/register",
        json={
            "email": "user@test.com",
            "password": "123456",
        },
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": "user@test.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()