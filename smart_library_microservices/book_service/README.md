# Book Service

Microservice for managing books in the Smart Library System.

## Features

- Create, read, update, and delete books
- Search books by title, author, ISBN, or genre
- Track available copies
- Update book availability for loans
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
uvicorn app.main:app --reload --port 8002
```

## API Endpoints

- `POST /api/books` - Create a new book
- `GET /api/books/{id}` - Get book by ID
- `PUT /api/books/{id}` - Update book
- `PATCH /api/books/{id}/availability` - Update book availability
- `DELETE /api/books/{id}` - Delete book
- `GET /api/books` - Search books (with pagination)
- `GET /health` - Health check

## API Documentation

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

## Testing

```bash
# Create a book
curl -X POST http://localhost:8002/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0-7432-7356-5",
    "genre": "Fiction",
    "copies": 3
  }'

# Get book
curl http://localhost:8002/api/books/1

# Search books
curl "http://localhost:8002/api/books?search=gatsby&page=1&per_page=10"

# Update availability
curl -X PATCH http://localhost:8002/api/books/1/availability \
  -H "Content-Type: application/json" \
  -d '{"operation": "decrement"}'
```

## Database Schema

```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    genre VARCHAR(100),
    copies INTEGER NOT NULL DEFAULT 1,
    available_copies INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_copies_positive CHECK (copies >= 0),
    CONSTRAINT check_available_copies_positive CHECK (available_copies >= 0),
    CONSTRAINT check_available_copies_not_exceed_copies CHECK (available_copies <= copies)
);
```
