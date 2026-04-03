

class Movimiento:

    def __init__(
        self,
        id,
        tipo,
        monto,
        fecha,
        descripcion=None,
        categoria=None,
        plataforma_id=None,
        plataforma_origen_id=None,
        plataforma_destino_id=None
    ):
        self.id = id
        self.tipo = tipo  # ingreso | gasto | permutacion
        self.monto = monto
        self.fecha = fecha
        self.descripcion = descripcion
        self.categoria = categoria
        self.plataforma_id = plataforma_id
        self.plataforma_origen_id = plataforma_origen_id
        self.plataforma_destino_id = plataforma_destino_id