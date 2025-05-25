# Loan Service

Microservice for managing book loans in the Smart Library System.

## Features

- Issue book loans
- Return books
- Extend loan periods
- Track overdue loans
- Integration with User and Book services
- Pagination support
- Health checks with dependency status

## Dependencies

This service depends on:
- **User Service**: To validate users
- **Book Service**: To check availability and update inventory

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

3. Ensure User Service (port 8001) and Book Service (port 8002) are running

4. Run the service:
```bash
uvicorn app.main:app --reload --port 8003
```

## API Endpoints

- `POST /api/loans` - Issue a new loan
- `POST /api/returns` - Return a book
- `PUT /api/loans/{id}/extend` - Extend a loan
- `GET /api/loans/{id}` - Get loan details
- `GET /api/loans/user/{user_id}` - Get user's loans
- `GET /api/loans` - List loans (with pagination)
- `GET /api/loans/overdue` - Get overdue loans
- `GET /health` - Health check with dependency status

## API Documentation

- Swagger UI: http://localhost:8003/docs
- ReDoc: http://localhost:8003/redoc

## Testing

```bash
# Issue a loan
curl -X POST http://localhost:8003/api/loans \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1,
    "due_date": "2025-06-01T00:00:00Z"
  }'

# Return a book
curl -X POST http://localhost:8003/api/returns \
  -H "Content-Type: application/json" \
  -d '{"loan_id": 1}'

# Extend a loan
curl -X PUT http://localhost:8003/api/loans/1/extend \
  -H "Content-Type: application/json" \
  -d '{"extension_days": 7}'

# Get user loans
curl http://localhost:8003/api/loans/user/1

# Get overdue loans
curl http://localhost:8003/api/loans/overdue
```

## Database Schema

```sql
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    return_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    extensions_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_loans_user_id ON loans(user_id);
CREATE INDEX idx_loans_book_id ON loans(book_id);
CREATE INDEX idx_loans_status ON loans(status);
```

## Business Rules

- Maximum loan period: 14 days (configurable)
- Maximum extensions: 2 (configurable)
- Extension period: 7 days (configurable)
- Users cannot borrow the same book twice simultaneously
- Books must be available to be borrowed
- Only active loans can be returned or extended
