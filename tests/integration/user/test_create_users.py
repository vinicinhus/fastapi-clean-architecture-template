from fastapi import status


def test_create_user_admin(client):
    """
    Testa a criação de um novo usuário.
    """
    payload = {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "password123",
        "full_name": "New User",
    }

    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
