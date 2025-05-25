# User Service

Microservice for managing users in the Smart Library System.

## Features

- Create, read, update, and delete users
- User roles: STUDENT, FACULTY, ADMIN
- Email validation and uniqueness
- Pagination support
- Health checks

## Running Locally

### Using Docker Compose

```bash
docker-compose up -d
```

### Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the service:
```bash
uvicorn app.main:app --reload --port 8001
```

## API Endpoints

- `POST /api/users` - Create a new user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
- `GET /api/users` - List users (with pagination)
- `GET /health` - Health check

## API Documentation

- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Testing

```bash
# Create a user
curl -X POST http://localhost:8001/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }'

# Get user
curl http://localhost:8001/api/users/1

# List users
curl "http://localhost:8001/api/users?page=1&per_page=10"
```

## Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
