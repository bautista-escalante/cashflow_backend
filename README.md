# 💸 CashFlow Backend

API REST para la gestión y seguimiento de flujo de caja personal o empresarial. Permite registrar movimientos financieros, administrar plataformas de pago y calcular permutaciones entre ellas, ofreciendo una visión clara del estado financiero en todo momento.

La API estará disponible en `https://cashflow-backend-bhya.onrender.com`.

La documentación interactiva (Swagger UI) en `https://cashflow-backend-bhya.onrender.com/docs`.
---

## 🚀 Tecnologías

| Tecnología | Uso |
|---|---|
| **Python** | Lenguaje principal |
| **FastAPI** | Framework web para la API REST |
| **SQLAlchemy** | ORM para la gestión de modelos y queries |
| **PostgreSQL** | Base de datos relacional |
| **Docker / Docker Compose** | Contenedorización de la base de datos |
| **dolarapi.com** | Cotización del dólar blue en tiempo real |

---

## 📌 Endpoints

### 💰 Movimientos

Los movimientos representan ingresos o gastos asociados a una plataforma.

---

#### `POST /movimiento`
Registra un nuevo movimiento (ingreso o gasto).

**Body:**
```json
{
  "tipo": "ingreso" | "gasto",
  "monto": 5000.0,
  "descripcion": "Sueldo de enero",
  "categoria": "trabajo",
  "plataforma_id": 1
}
```

**Response `200`:**
```json
{
  "id": 1,
  "tipo": "ingreso",
  "monto": 5000.0,
  "fecha": "2024-01-15",
  "descripcion": "Sueldo de enero",
  "categoria": "trabajo",
  "plataforma_id": 1
}
```

**Response `400`:** Error de validación o plataforma inexistente.

---

#### `GET /movimientos`
Retorna todos los movimientos registrados (ingresos y gastos).

**Response `200`:** Lista de objetos `MovimientoResponse`.

---

#### `GET /movimientos/gastos`
Retorna únicamente los movimientos de tipo `gasto`.

**Response `200`:** Lista de objetos `MovimientoResponse`.

---

#### `GET /movimientos/ingresos`
Retorna únicamente los movimientos de tipo `ingreso`.

**Response `200`:** Lista de objetos `MovimientoResponse`.

---

#### `GET /movimientos/evolucion`
Retorna la evolución del saldo acumulado a lo largo del tiempo, agrupada por fecha. Permite visualizar el historial financiero como una línea de tiempo.

**Response `200`:**
```json
[
  { "fecha": "2024-01-10", "saldo": 3000.0 },
  { "fecha": "2024-01-15", "saldo": 8000.0 },
  { "fecha": "2024-01-20", "saldo": 6500.0 }
]
```

> El saldo es acumulativo: suma los ingresos y resta los gastos día a día en orden cronológico.

---

#### `GET /movimiento/{movimiento_id}`
Retorna un movimiento específico por su ID.

**Path param:** `movimiento_id` — ID entero del movimiento.

**Response `200`:** Objeto `MovimientoResponse`.  
**Response `400`:** Si no se encuentra el movimiento.

---

### 🏦 Plataformas

Las plataformas representan billeteras, cuentas bancarias o cualquier medio de pago donde se almacena saldo.

---

#### `POST /plataforma`
Crea una nueva plataforma con un saldo inicial.

**Body:**
```json
{
  "nombre": "mercadopago",
  "saldo": 10000.0
}
```

**Response `201`:**
```json
{
  "id": 1,
  "nombre": "mercadopago",
  "saldo": 10000.0,
  "fecha_creacion": "2024-01-15T10:00:00"
}
```

**Response `400`:** Si ya existe una plataforma con ese nombre.

---

#### `GET /plataformas`
Retorna todas las plataformas registradas.

**Response `200`:** Lista de objetos `PlataformaResponse`.

---

#### `GET /plataforma/{nombre}`
Retorna una plataforma por su nombre. El nombre se normaliza automáticamente (minúsculas, sin espacios).

**Path param:** `nombre` — Nombre de la plataforma (ej: `mercadopago`).

**Response `200`:** Objeto `PlataformaResponse`.  
**Response `400`:** `"No se encontró la plataforma."`

---

### 🔄 Permutaciones

Las permutaciones transfieren saldo entre dos plataformas, registrando el movimiento automáticamente.

---

#### `POST /permutacion`
Transfiere un monto desde una plataforma origen hacia una plataforma destino en la misma moneda.

El saldo de la plataforma origen se reduce y el de la destino se incrementa. Se genera automáticamente un `Movimiento` con la descripción `"cambio de {origen} a {destino}"`.

**Body:**
```json
{
  "tipo": "permutacion",
  "monto": 2000.0,
  "plataforma_origen_id": 1,
  "plataforma_destino_id": 2
}
```

**Response `200`:** Objeto `PermutacionResponse`.  
**Response `400`:** Si el saldo es insuficiente u origen/destino son inválidos.  
**Response `500`:** Error interno del servidor.

---

#### `POST /permutacion_dolar`
Realiza una compra o venta de dólares entre plataformas, aplicando la cotización del **dólar blue en tiempo real** (via [dolarapi.com](https://dolarapi.com)).

El tipo de operación se determina automáticamente según el nombre de las plataformas:

| Operación | Condición | Cotización aplicada |
|-----------|-----------|---------------------|
| **Compra** | Plataforma destino se llama `"dolares"` | Precio de venta del blue |
| **Venta** | Plataforma origen se llama `"dolares"` | Precio de compra del blue |

**Body:**
```json
{
  "tipo": "permutacion_dolar",
  "monto": 100.0,
  "plataforma_origen_id": 1,
  "plataforma_destino_id": 3
}
```

**Response `200`:**
```json
{
  "id": 0,
  "tipo": "permutacion_dolar",
  "monto": 100.0,
  "fecha": "2024-01-15",
  "plataforma_origen_id": 1,
  "plataforma_destino_id": 3,
  "valor_cambio": 1215.0
}
```

> `valor_cambio` refleja la cotización del dólar blue utilizada al momento exacto de la operación.

**Response `400`:** Saldo insuficiente o validación fallida.  
**Response `500`:** Error interno (ej: fallo al consultar la API de cotización).

---

## 📋 Resumen de endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/movimiento` | Registrar un movimiento |
| `GET` | `/movimientos` | Listar todos los movimientos |
| `GET` | `/movimientos/gastos` | Listar solo gastos |
| `GET` | `/movimientos/ingresos` | Listar solo ingresos |
| `GET` | `/movimientos/evolucion` | Evolución del saldo en el tiempo |
| `GET` | `/movimiento/{id}` | Obtener movimiento por ID |
| `POST` | `/plataforma` | Crear una plataforma |
| `GET` | `/plataformas` | Listar todas las plataformas |
| `GET` | `/plataforma/{nombre}` | Obtener plataforma por nombre |
| `POST` | `/permutacion` | Transferir saldo entre plataformas |
| `POST` | `/permutacion_dolar` | Comprar/vender dólares blue |

---

## 🏗️ Arquitectura

El proyecto sigue una arquitectura en capas inspirada en los principios de **Clean Architecture**, separando claramente las responsabilidades en tres módulos principales:

```
cashflow_backend/
│
├── main.py                        # Punto de entrada de la aplicación
│
├── api/                           # Capa de presentación
│   └── routes/                    # Definición de endpoints REST
│       ├── Movimiento_routes.py
│       ├── Plataforma_routes.py
│       └── permutacion_routes.py
│
├── core/                          # Capa de dominio / lógica de negocio
│   └── models/                    # Modelos de dominio (entidades)
│       ├── Movimiento.py
│       └── Plataforma.py
│
└── infrastructure/                # Capa de infraestructura
    └── database/
        └── db.py                  # Configuración de SQLAlchemy y conexión a PostgreSQL
```

### Descripción de capas

**`api/`** — Capa de presentación. Contiene los routers de FastAPI que exponen los endpoints HTTP. Es la única capa que interactúa directamente con las requests y responses.

**`core/`** — Capa de dominio. Define los modelos de datos (entidades) usando SQLAlchemy ORM. Aquí reside la lógica central del negocio, independiente de frameworks externos.

**`infrastructure/`** — Capa de infraestructura. Maneja la configuración de la base de datos, el engine de SQLAlchemy y la sesión de conexión a PostgreSQL.

---

## 🗄️ Base de datos

La base de datos es **PostgreSQL**, gestionada mediante **SQLAlchemy** como ORM. La conexión y el engine se configuran en `infrastructure/database/db.py`. Las tablas se crean automáticamente al iniciar la aplicación a través de `Base.metadata.create_all(bind=engine)`.


---


## 📄 Licencia

Este proyecto es de uso personal/educativo. No cuenta con una licencia específica por el momento.
