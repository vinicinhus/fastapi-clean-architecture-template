from fastapi import status


def test_list_users(client):
    """
    Testa a listagem de usuários existentes.
    """
    response = client.get("/api/v1/users/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # Deve conter ao menos o mock_current_user
