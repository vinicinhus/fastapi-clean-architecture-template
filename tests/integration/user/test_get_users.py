from fastapi import status

def test_get_user_by_id(client, mock_current_user_admin):
    """
    Testa a recuperação de um usuário pelo ID.
    """
    user_id = mock_current_user_admin.id
    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == mock_current_user_admin.email
    
def test_get_user_by_email(client, mock_current_user):
    """
    Testa a recuperação de um usuário pelo email.
    """
    response = client.get(f"/api/v1/users/email/{mock_current_user.email}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == mock_current_user.email
