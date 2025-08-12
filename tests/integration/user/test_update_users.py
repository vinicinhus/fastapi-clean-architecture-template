from fastapi import status


def test_update_user(client, mock_current_user):
    """
    Testa a atualização de um usuário existente.
    """
    payload = {
        "username": "admin_updated",
        "email": "admin_updated@example.com",
        "full_name": "Admin Updated User"
    }

    response = client.put(f"/api/v1/users/{mock_current_user.id}", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
