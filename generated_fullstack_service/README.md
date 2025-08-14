# Full-Stack Web Service

A task management application built with Go backend and React frontend.

## Quick Start

### Prerequisites
- Go 1.19+
- Node.js 18+
- Docker & Docker Compose
- Tilt (https://tilt.dev)

### Development with Tilt
```bash
tilt up
```

### Manual Development
```bash
# Terminal 1 - Backend
cd backend
go mod tidy
go run main.go

# Terminal 2 - Frontend  
cd frontend
npm install
npm start
```

## Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Tilt UI: http://localhost:10350

## API Endpoints
- GET /health - Health check
- GET /tasks - List all tasks
- POST /tasks - Create a task
- PUT /tasks/:id - Update a task
- DELETE /tasks/:id - Delete a task
