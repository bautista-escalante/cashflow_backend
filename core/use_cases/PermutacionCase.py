from sqlalchemy.orm import Session

from core.models.Plataforma import Plataforma
from api.schemas.PermutacionSchema import PermutacionCreate
from core.validators.MovimientoValidator import MovimientoValidator

class PermutacionCase:

    def generar_permutaciones(self, db:Session, permutacion: PermutacionCreate):

        origen = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_origen_id
        ).first()

        destino = db.query(Plataforma).filter(
            Plataforma.id == permutacion.plataforma_destino_id
        ).first()

        MovimientoValidator.validar_permutacion(permutacion, origen, destino, permutacion)
        
        origen.saldo -= permutacion.monto
        destino.saldo += permutacion.monto

        db.commit()

        return {"mensaje": "Permutación realizada correctamente"}
    
    """ 
    primero: obtener el valor que hay en dichas plataformas
    segundo: restarle el monto a la plataforma origen y sumarle el monto a la plataforma destino,
    tercero: guardar el movimiento en la db
    """
