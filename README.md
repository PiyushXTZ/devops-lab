# DevOps Lab — Git + Docker
# DevOps Lab — Git + Docker

![CI](https://github.com/mohammedadnan-10/devops-lab/actions/workflows/ci.yml/badge.svg)

A Flask + Redis + Nginx stack running on Docker Compose.

## Services
- **Nginx** — reverse proxy on port 80
- **Flask** — visit counter app on port 5000
- **Redis** — persistent storage for the counter

## Quick Start
```bash
docker compose up --build -d
curl http://localhost
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| /        | GET    | Increment and return visit count |
| /reset   | POST   | Reset visit counter to zero |
| /stats   | GET    | Return full stats |
| /health  | GET    | Health check |
