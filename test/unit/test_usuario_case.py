from fastapi import HTTPException
import pytest

from api.schemas.UsuarioSchema import UsuarioCreate

from core.use_cases.UsuarioCase import UsuarioCase

def test_crear_usuario(db):
    usuario_prueba = UsuarioCreate(
        nombre="Usuario de prueba",
        email="usuario@prueba.com",
        clave="clave_de_prueba"
    )

    usuario_case = UsuarioCase()
    result = usuario_case.crear_usuario(usuario_prueba, db)

    assert result is not None

def test_crear_usuario_fallido(db):
    usuario_prueba_fallida = UsuarioCreate(
        nombre="Usuario de prueba",
        email="usuario@prueba.com",
        clave="1"
    )

    usuario_case = UsuarioCase()
    with pytest.raises(HTTPException):
        usuario_case.crear_usuario(usuario_prueba_fallida, db)

def test_crear_usuario_duplicado(db):
    usuario_prueba_duplicado = UsuarioCreate(
        nombre="Usuario de prueba duplicado",
        email="usuarioDuplicado@prueba.com",
        clave="clave_de_prueba"
    )

    usuario_case = UsuarioCase()
    usuario_case.crear_usuario(usuario_prueba_duplicado, db)

    with pytest.raises(HTTPException):
        usuario_case.crear_usuario(usuario_prueba_duplicado, db)


def test_modificar_usuario(db):
    usuario_case = UsuarioCase()
    usuario_prueba = UsuarioCreate(
        nombre="Usuario de prueba para modificar",
        email="usuarioModificar@prueba.com",
        clave="clave_de_prueba"
    )
    usuario_prueba = usuario_case.crear_usuario(usuario_prueba, db)

    usuario_modificado = usuario_case.actualizar_usuario("nueva_clave", usuario_prueba.id, db)

    assert usuario_modificado is not None


def test_eliminar_usuario(db):
    usuario_case = UsuarioCase()
    usuario_prueba = UsuarioCreate(
        nombre="Usuario de prueba para eliminar",
        email="usuarioEliminar@prueba.com",
        clave="clave_de_prueba"
    )

    usuario_prueba = usuario_case.crear_usuario(usuario_prueba, db)

    usuario_case.eliminar_usuario(usuario_prueba.id, db)
    with pytest.raises(HTTPException):
        usuario_case.obtener_usuario(usuario_prueba.id, db)


def test_obtener_usuario(db):
    usuario_case = UsuarioCase()
    usuario_prueba = UsuarioCreate(
        nombre="Usuario de prueba para obtener",
        email="usuarioObtener@prueba.com",
        clave="clave_de_prueba"
    )

    usuario_prueba = usuario_case.crear_usuario(usuario_prueba, db)

    usuario_obtenido = usuario_case.obtener_usuario(usuario_prueba.id, db)

    assert usuario_obtenido is not None
