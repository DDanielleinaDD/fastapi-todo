from conftest import client


def test_register():
    response = client.post('/auth/register',
                           json={
                            "email": "a1111@example.com",
                            "password": "string",
                            "is_active": True,
                            "is_superuser": False,
                            "is_verified": False,
                            "username": "a11111"
                            })
    assert response.status_code == 201, ('Ошибка регистрации, проверьте'
                                         ' валидность данных или такой'
                                         ' пользователь уже существует.')
    assert "a1111@example.com" == (response.json()['email'],
                                   'Пользователя с таким email не существует.')
