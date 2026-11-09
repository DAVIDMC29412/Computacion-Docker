# SuspensionPro · CRUD de repuestos de suspensión

Aplicación en Docker con **FastAPI + MySQL + Nginx** para administrar un inventario de repuestos de suspensión (amortiguadores, espirales, bujes, rótulas…).

## Estructura

```
docker-final/
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py       # Endpoints CRUD
│       ├── models.py     # Modelo Repuesto (SQLAlchemy)
│       ├── schemas.py    # Validación (Pydantic)
│       └── database.py
├── frontend/index.html   # Interfaz web
└── nginx/default.conf    # Sirve el frontend y redirige /api a FastAPI
```

## Endpoints

| Método | Ruta                    | Acción              |
|--------|-------------------------|---------------------|
| GET    | `/api/repuestos`        | Listar (filtros `q`, `tipo`) |
| GET    | `/api/repuestos/{id}`   | Ver uno             |
| POST   | `/api/repuestos`        | Agregar             |
| PUT    | `/api/repuestos/{id}`   | Editar              |
| DELETE | `/api/repuestos/{id}`   | Eliminar            |

Documentación interactiva: `http://localhost/docs`

## Ejecutar en local

```bash
docker compose up -d --build
```

Abrir `http://localhost`.

## Subir a GitHub

```bash
git remote add origin https://github.com/TU_USUARIO/suspension-crud.git
git branch -M main
git push -u origin main
```

## Desplegar en AWS (EC2)

1. Crear una instancia EC2 (Ubuntu 24.04, t2.micro o t3.micro).
2. En el **Security Group** abrir los puertos **22** (SSH) y **80** (HTTP).
3. Conectarse por SSH e instalar Docker:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
   sudo usermod -aG docker ubuntu && newgrp docker
   ```
4. Clonar y levantar:
   ```bash
   git clone https://github.com/TU_USUARIO/suspension-crud.git
   cd suspension-crud
   docker compose up -d --build
   ```
5. Abrir `http://IP_PUBLICA_DE_LA_EC2`.

> Para producción cambia las contraseñas de MySQL en `docker-compose.yml` (idealmente con un archivo `.env`).
