from core.use_cases.PlataformaCase import PlataformaCase
from api.schemas.PlataformaSchema import PlataformaCreate
from api.schemas.UsuarioSchema import UsuarioResponse

from fastapi import HTTPException
import pytest

def test_crear_plataforma(db, usuario_prueba: UsuarioResponse):

    plataforma_case = PlataformaCase()

    plataforma_data = PlataformaCreate(nombre="efectivo", saldo=100.0)

    result = plataforma_case.crear_plataforma(db, plataforma_data, usuario_prueba.id)

    assert PlataformaCreate.model_validate(result) is not None

def test_crear_plataforma_duplicada(db, usuario_prueba: UsuarioResponse):

    plataforma_case = PlataformaCase()

    plataforma_data = PlataformaCreate(nombre="efectivo", saldo=100.0)

    result = plataforma_case.crear_plataforma(db, plataforma_data, usuario_prueba.id)

    with pytest.raises(HTTPException):
        plataforma_case.crear_plataforma(db, plataforma_data, usuario_prueba.id)