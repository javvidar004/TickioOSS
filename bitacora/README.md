# Bitácora del Equipo — TickioOSS

Registro cronológico de avances, decisiones técnicas y obstáculos del proyecto.

---

## Semana 1 — Planificación y Setup (mayo 2026)

### Decisiones tomadas
- **Stack elegido:** FastAPI (Python) + React + PostgreSQL + Docker
  - FastAPI por su velocidad, tipado estático y documentación automática (Swagger)
  - React para una SPA moderna con routing del lado del cliente
  - PostgreSQL como base de datos relacional robusta y OSS
  - Docker para garantizar reproducibilidad del entorno

- **Licencia:** MIT — permite uso libre, modificación y redistribución
- **Arquitectura:** Tres capas separadas (frontend, backend, base de datos) en contenedores independientes
- **Roles de usuario:** Tres niveles — user (reporta), agent (atiende), admin (administra)

### Avances
- Estructura inicial del repositorio creada con carpetas Backend, Frontend, DB
- Configuración de Dockerfiles y docker-compose
- Modelos de base de datos definidos: `users`, `tickets`, `comments`
- API REST implementada con autenticación JWT
- Frontend con React Router, páginas de Login, Tickets, Dashboard y Admin

### Obstáculos encontrados
- **Problema:** Configurar CORS entre FastAPI y React en desarrollo local
  - **Solución:** Proxy de Vite (`/api → localhost:8000`) para evitar problemas de CORS en dev
- **Problema:** Inicialización del admin en Docker (la BD se crea antes de que las tablas existan)
  - **Solución:** Script `init.sql` que inserta el admin con `ON CONFLICT DO NOTHING` después de que SQLAlchemy crea las tablas

---

## Semana 2 — Desarrollo e Integración

### Avances
- Módulo de tickets completo (CRUD + filtros + paginación implícita por orden)
- Sistema de comentarios en tickets
- Dashboard con estadísticas en tiempo real
- Panel de administración de usuarios (cambio de rol, activar/desactivar, eliminar)
- Suite de tests automatizados con pytest + TestClient
- Documentación completa: README, CONTRIBUTING, Architecture diagram, API docs (Swagger)

### Qué salió bien
- La separación de responsabilidades (routers/schemas/models) facilitó el desarrollo paralelo
- FastAPI generó documentación interactiva automáticamente (`/docs`)
- Vite proxy eliminó la necesidad de configurar CORS manualmente en desarrollo

### Qué ajustamos
- Cambiamos de SQLite a PostgreSQL desde el inicio para evitar problemas al migrar a Docker
- Agregamos el campo `updated_at` al modelo Ticket después de notar que era necesario para detectar cambios recientes
