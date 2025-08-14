.PHONY: setup install clean dev backend frontend docker-build docker-run test

# Setup the project
setup: install

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && go mod tidy
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Clean build artifacts
clean:
	cd backend && go clean
	cd frontend && rm -rf build/ node_modules/.cache/

# Development with hot reload (requires two terminals)
dev:
	@echo "Starting development servers..."
	@echo "Run 'make backend' in one terminal and 'make frontend' in another"

# Start backend server
backend:
	cd backend && go run main.go

# Start frontend development server  
frontend:
	cd frontend && npm start

# Build and run with Docker Compose
docker-build:
	docker-compose build

docker-run: docker-build
	docker-compose up

# Run with Tilt (requires Tilt and Kubernetes)
tilt:
	tilt up

# Test the application
test:
	@echo "Testing backend..."
	cd backend && go test ./...
	@echo "Testing frontend..."  
	cd frontend && npm test -- --watchAll=false

# Build for production
build:
	@echo "Building backend..."
	cd backend && go build -o main .
	@echo "Building frontend..."
	cd frontend && npm run build

help:
	@echo "Available commands:"
	@echo "  setup        - Install all dependencies"
	@echo "  install      - Install dependencies" 
	@echo "  clean        - Clean build artifacts"
	@echo "  dev          - Instructions for development"
	@echo "  backend      - Start backend server"
	@echo "  frontend     - Start frontend server"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  tilt         - Run with Tilt"
	@echo "  test         - Run tests"
	@echo "  build        - Build for production"
# Makefile
build-backend:
	docker build -t task-management-backend:latest ./backend

build-frontend:
	docker build -t task-management-frontend:latest ./frontend

deploy:
	kubectl apply -f deployment.yaml

up:
	docker-compose up

down:
	docker-compose down
