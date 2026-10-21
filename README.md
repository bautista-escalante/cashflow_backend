# 💸 CashFlow Backend

[![CI](https://github.com/bautista-escalante/cashflow_backend/actions/workflows/ci.yml/badge.svg)](https://github.com/bautista-escalante/cashflow_backend/actions)
![Python](https://img.shields.io/badge/Python-3.[X]-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791)


> 🇬🇧 **English summary:** REST API to track personal cash flow across multiple payment platforms (bank accounts, wallets, cash). It records income and expenses, transfers balance between platforms, and handles USD ↔ ARS exchanges using the real-time "blue dollar" rate (a parallel exchange rate widely used in Argentina). Built with **Python, FastAPI, SQLAlchemy, PostgreSQL and Docker**, with layered architecture inspired by Clean Architecture, automated tests, CI on GitHub Actions, database migrations with Alembic, and continuous deployment on Render.

API REST para llevar el flujo de caja personal repartido en distintas plataformas de pago (billeteras virtuales, cuentas bancarias, efectivo). Registra ingresos y gastos, transferencias entre plataformas y compra/vende dólares aplicando la cotización del **dólar blue en tiempo real**.

🔗 **API en producción:** https://cashflow-backend-bhya.onrender.com

📖 **Documentación interactiva (Swagger):** https://cashflow-backend-bhya.onrender.com/docs

🖥️ **Frontend (Angular/Ionic):** (https://github.com/bautista-escalante/cashflow_frontend)

> ⏳ El servidor está en el plan gratuito de Render: si estuvo inactivo, la primera request puede tardar unos segundos en responder.

<img width="1895" height="860" alt="docs" src="https://github.com/user-attachments/assets/b5207a85-621f-4342-bf24-e7c02699032a" />

---

## ✨ Qué hace

- **Movimientos:** registra ingresos y gastos asociados a una plataforma, filtrables por tipo.
- **Evolución del saldo:** calcula el saldo acumulado día a día para graficar el historial financiero.
- **Plataformas:** administra billeteras y cuentas con su saldo; los nombres se normalizan para evitar duplicados.
- **Permutaciones:** transfiere saldo entre plataformas y genera el movimiento automáticamente.
- **Compra/venta de dólares:** detecta si es compra o venta según la plataforma involucrada y guarda la cotización usada en cada operación.

---

## 🚀 Stack tecnológico

| Tecnología | Para qué la uso | Por qué |
| --- | --- | --- |
| **Python + FastAPI** | API REST | Validación automática con Pydantic y documentación Swagger sin configuración extra |
| **SQLAlchemy** | ORM | Modelos y queries desacoplados del motor de base de datos |
| **PostgreSQL** | Base de datos | Alojada en Supabase: persiste mientras el proyecto esté activo y se puede inspeccionar online desde su panel|
| **Alembic** | Migraciones | Versionar los cambios del esquema en lugar de crear tablas al arrancar |
| **Docker / Docker Compose** | Contenedores | Entorno reproducible para la app y la base |
| **pytest** | Tests | tests automatizados unitarios y de integracion |
| **GitHub Actions** | CI | Corre los tests en cada push |
| **Render** | Deploy | Despliegue automático desde `main` |
| **dolarapi.com** | API externa | Cotización del dólar blue en tiempo real |

---

## 🏗️ Arquitectura

El proyecto sigue una **arquitectura en capas inspirada en Clean Architecture**, con el objetivo de separar responsabilidades y que cada capa pueda cambiar sin arrastrar a las demás.

<img width="982" height="477" alt="diagrama" src="https://github.com/user-attachments/assets/54ddb34e-b777-4557-b198-bf090e58cc42" />

```
cashflow_backend/
├── main.py                  # Punto de entrada
├── api/routes/              # Presentación: endpoints REST (FastAPI)
├── core/models/             # Dominio: entidades y reglas de negocio
├── infrastructure/database/ # Infraestructura: conexión y sesión de PostgreSQL
├── test/                    # Tests automatizados
├── .github/workflows/       # Pipeline de CI
├── Dockerfile
└── docker-compose.yml
```

- **`api/`** recibe las requests, valida y responde. Es la única capa que conoce HTTP.
- **`core/`** contiene las entidades y la lógica del negocio (por ejemplo, las reglas de una permutación).
- **`infrastructure/`** maneja todo lo externo: base de datos [y la llamada a dolarapi, CONFIRMAR dónde vive].

---

## 🧠 Decisiones técnicas

- **Migraciones con Alembic en vez de `create_all`:** el esquema de la base queda versionado en el repo. Si el proyecto de Supabase se pausa o hay que recrear la base, `alembic upgrade head` reconstruye todas las tablas en un solo paso, y los cambios futuros del esquema se aplican sin perder datos.
- **Base en Supabase, API en Render:** la base gratuita de Render se eliminó dos veces aunque el proyecto estaba en uso. En Supabase los datos persisten mientras el proyecto esté activo y se pueden inspeccionar online desde su panel.
- **Se guarda `valor_cambio` en cada operación en dólares:** el historial conserva la cotización exacta usada en ese momento, aunque el dólar cambie después.

---

## ✅ Tests y CI/CD

- Los tests viven en `test/` y cubren crud a usuarios, plataformas, movimentos(reglas de negocio) y endpoints(integracion).
- **GitHub Actions** ejecuta la suite en cada push y reporta si pasó o falló.
- **Render** despliega automáticamente desde `main`. Hoy el deploy es independiente del resultado del CI.

Correr los tests en local:

```bash
 python -m pytest -s
```

<img width="1417" height="432" alt="test" src="https://github.com/user-attachments/assets/255bd6b5-b422-414a-b091-3752a9e11069" />

---

## 📌 Endpoints

La referencia completa e interactiva está en **[Swagger](https://cashflow-backend-bhya.onrender.com/docs)**. Resumen:

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/movimiento` | Registrar un ingreso o gasto |
| `GET` | `/movimientos` | Listar todos los movimientos |
| `GET` | `/movimientos/gastos` | Listar solo gastos |
| `GET` | `/movimientos/ingresos` | Listar solo ingresos |
| `GET` | `/movimientos/evolucion` | Evolución del saldo en el tiempo |
| `GET` | `/movimiento/{id}` | Obtener un movimiento |
| `POST` | `/plataforma` | Crear una plataforma con saldo inicial |
| `GET` | `/plataformas` | Listar plataformas |
| `GET` | `/plataforma/{nombre}` | Obtener plataforma por nombre |
| `POST` | `/permutacion` | Transferir saldo entre plataformas |
| `POST` | `/permutacion_dolar` | Comprar/vender dólares blue |

<details>
<summary><b>Ejemplo: compra/venta de dólares (<code>POST /permutacion_dolar</code>)</b></summary>

La operación se determina por el nombre de las plataformas:

| Operación | Condición | Cotización aplicada |
| --- | --- | --- |
| **Compra** | La plataforma destino se llama `dolares` | Precio de venta del blue |
| **Venta** | La plataforma origen se llama `dolares` | Precio de compra del blue |

Request:

```json
{
  "tipo": "permutacion_dolar",
  "monto": 100.0,
  "plataforma_origen_id": 1,
  "plataforma_destino_id": 3
}
```

Response:

```json
{
  "id": 1,
  "tipo": "permutacion_dolar",
  "monto": 100.0,
  "fecha": "2024-01-15",
  "plataforma_origen_id": 1,
  "plataforma_destino_id": 3,
  "valor_cambio": 1215.0
}
```

</details>

<details>
<summary><b>Ejemplo: evolución del saldo (<code>GET /movimientos/evolucion</code>)</b></summary>

El saldo es acumulativo: suma ingresos y resta gastos día a día en orden cronológico.

```json
[
  { "fecha": "2024-01-10", "saldo": 3000.0 },
  { "fecha": "2024-01-15", "saldo": 8000.0 },
  { "fecha": "2024-01-20", "saldo": 6500.0 }
]
```

</details>

---

## 👤 Autor

**Bautista Escalante**, desarrollador backend Python.

- 💼 Portfolio: https://bautistaescalante.vercel.app/VisualPort
- 🐙 GitHub: https://github.com/bautista-escalanteo
