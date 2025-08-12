from fastapi import status


def test_delete_user(client):
    """
    Testa a exclusão de um usuário.
    """
    response = client.delete(f"/api/v1/users/2")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verifica se o usuário foi removido
    response_check = client.get(f"/api/v1/users/2")
    assert response_check.status_code == status.HTTP_404_NOT_FOUND
