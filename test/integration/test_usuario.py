
from fastapi.testclient import TestClient

from api.schemas.UsuarioSchema import UsuarioCreate

from core.models.Usuario import Usuario
from core.models.Plataforma import Plataforma
from core.models.Movimiento import Movimiento


def test_create_user(client: TestClient, db):

    usuario = UsuarioCreate(
        nombre="Usuario prueba344",
        email="test@example344.com",
        clave="clave_de_prueba"
    )

    print(f"Usuario de prueba: {usuario.model_dump()}")
    response = client.post("/usuarios/",  json=usuario.model_dump())
    print(f"Respuesta de creación: {response.json()}")

    assert response.status_code == 200


def test_authenticate_user(client: TestClient, usuario_prueba):
    print(f"Usuario de prueba: {usuario_prueba.model_dump()}")
    print(f"Email: {usuario_prueba.email}")
    auth_data = {
        "email": usuario_prueba.email,
        "clave": "clave_de_prueba"
    }

    response = client.post("/usuarios/auth", json=auth_data)
    print(f"Respuesta de autenticación: {response.json()}")

    assert response.status_code == 200
    assert "access_token" in response.json()



