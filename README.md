# 🎫 TickioOSS

**Open-source IT support ticket system** built with FastAPI, React, and PostgreSQL.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docker.com)

---

## What is TickioOSS?

TickioOSS is a web-based IT support ticketing platform that allows organizations to:

- **Users** — report IT incidents (hardware failures, software bugs, network issues, access problems)
- **Agents** — manage, assign, and resolve tickets
- **Admins** — full control over users, roles, and the system

Built entirely with open-source technologies as part of the final project for *Sistemas y Lenguajes de Código Abierto* at Universidad Panamericana.

---

## Features

| Module | Description |
|---|---|
| Authentication | JWT-based login/register with role-based access control (user / agent / admin) |
| Ticket Management | Create, view, filter, update status/priority/category, assign, delete tickets |
| Comments | Add threaded comments to any ticket |
| Dashboard | Real-time stats on ticket volume, status distribution, and priority breakdown |
| User Admin | Admin panel to manage users, change roles, enable/disable accounts |

---

## Tech Stack (100% OSS)

| Layer | Technology | License |
|---|---|---|
| Backend | Python 3.12 + FastAPI | MIT |
| ORM | SQLAlchemy 2.0 | MIT |
| Database | PostgreSQL 16 | PostgreSQL License |
| Auth | python-jose + passlib + bcrypt | MIT |
| Frontend | React 18 + Vite | MIT |
| Styling | TailwindCSS 3 | MIT |
| HTTP Client | Axios | MIT |
| Router | React Router v6 | MIT |
| Container | Docker + docker-compose | Apache 2.0 |
| Web server | Nginx | BSD |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Browser                         │
│              React + Vite + Tailwind                │
│                  (port 3000)                        │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP /api/*
                       ▼
┌─────────────────────────────────────────────────────┐
│              Nginx (reverse proxy)                  │
│  static files + proxy /api → backend:8000           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│           FastAPI Backend (port 8000)               │
│                                                     │
│  /auth    → Auth router (register, login, me)       │
│  /tickets → Tickets router (CRUD + comments)        │
│  /users   → Users router (admin only)               │
│                                                     │
│  SQLAlchemy ORM  │  JWT auth  │  Pydantic schemas   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           PostgreSQL 16 (port 5432)                 │
│                                                     │
│  tables: users, tickets, comments                   │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start (Docker — recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes docker-compose)
- Git

### 1. Clone the repository
```bash
git clone https://github.com/javvidar004/TickioOSS.git
cd TickioOSS
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env to change SECRET_KEY for production
```

### 3. Start all services
```bash
docker compose up --build
```

### 4. Open the app
| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API docs | http://localhost:8000/docs |
| API health | http://localhost:8000/health |

### Default credentials
| Username | Password | Role |
|---|---|---|
| admin | admin123 | admin |

> **Change the admin password immediately after first login.**

---

## Manual Installation (without Docker)

### Backend

```bash
cd Backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

# Set environment variables
set DATABASE_URL=postgresql://user:pass@localhost:5432/tickio_db
set SECRET_KEY=your-secret-key

uvicorn app.main:app --reload
```

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

The frontend dev server runs on http://localhost:5173 and proxies API calls to http://localhost:8000.

---

## API Reference

Full interactive docs at http://localhost:8000/docs (Swagger UI).

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /auth/register | — | Create account |
| POST | /auth/login | — | Get JWT token |
| GET | /auth/me | user | Current user info |
| GET | /tickets/ | user | List tickets (filtered by role) |
| POST | /tickets/ | user | Create ticket |
| GET | /tickets/dashboard | user | Stats summary |
| GET | /tickets/{id} | user | Get ticket detail |
| PUT | /tickets/{id} | user/agent | Update ticket |
| DELETE | /tickets/{id} | admin/owner | Delete ticket |
| GET | /tickets/{id}/comments | user | List comments |
| POST | /tickets/{id}/comments | user | Add comment |
| GET | /users/ | admin | List all users |
| PUT | /users/{id} | admin | Update user role/status |
| DELETE | /users/{id} | admin | Delete user |

---

## Running Tests

```bash
cd Backend
pip install -r requirements.txt
pytest tests/ -v
```

---

## Project Structure

```
TickioOSS/
├── Backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── config.py        # Settings (env vars)
│   │   ├── database.py      # SQLAlchemy engine + session
│   │   ├── auth/
│   │   │   └── jwt.py       # Password hashing + JWT helpers
│   │   ├── models/
│   │   │   ├── user.py      # User model + UserRole enum
│   │   │   └── ticket.py    # Ticket, Comment models + enums
│   │   ├── schemas/
│   │   │   ├── user.py      # Pydantic schemas for users
│   │   │   └── ticket.py    # Pydantic schemas for tickets
│   │   └── routers/
│   │       ├── auth.py      # /auth endpoints
│   │       ├── tickets.py   # /tickets endpoints
│   │       └── users.py     # /users endpoints
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_tickets.py
│   ├── requirements.txt
│   └── Dockerfile
├── Frontend/
│   ├── src/
│   │   ├── App.jsx          # Routes
│   │   ├── api/axios.js     # Axios instance + interceptors
│   │   ├── context/         # Auth context
│   │   ├── components/      # Navbar, PrivateRoute, badges
│   │   └── pages/           # Login, Register, Tickets, Dashboard, Admin
│   ├── nginx.conf
│   ├── package.json
│   └── Dockerfile
├── DB/
│   ├── init.sql             # Seed data (admin user)
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

---

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Team

| Name | Role |
|---|---|
| Gabriel Sosa | Backend / Auth |
| Javier | Frontend / UI |
| [Team members] | Database / DevOps |

*Universidad Panamericana — Sistemas y Lenguajes de Código Abierto*
