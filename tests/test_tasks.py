import pytest


@pytest.mark.asyncio
async def test_create_task(client):

    await client.post(
        "/auth/register",
        json={
            "email": "task@test.com",
            "password": "123456",
        },
    )

    login = await client.post(
        "/auth/login",
        data={
            "username": "task@test.com",
            "password": "123456",
        },
    )

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = await client.post(
        "/tasks",
        json={
            "title": "Test",
            "description": "Desc",
            "status": "new",
            "deadline": None,
        },
        headers=headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test"