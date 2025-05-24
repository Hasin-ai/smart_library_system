# Smart Library System

A modern FastAPI-based library management system with comprehensive book, user, and loan management capabilities.

## Features

- **User Management**: Handle students, faculty, and admin users
- **Book Management**: Add, update, search, and manage book inventory  
- **Loan System**: Issue, return, and extend book loans
- **Statistics**: Track popular books, active users, and system overview
- **RESTful API**: Clean, well-documented API endpoints

## Quick Start

### Option 1: Automated Setup
```bash
cd smart_library_system
python setup.py          # Installs deps, sets up DB, seeds data
python run.py             # Starts the server
```

### Option 2: Manual Setup
```bash
cd smart_library_system
pip install -r requirements.txt
cp .env.example .env      # Edit database URL if needed
python scripts/init_db.py
python scripts/seed_data.py
uvicorn app.main:app --reload
```

### Access Points
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Users
- `POST /api/users/` - Create user
- `GET /api/users/` - List users  
- `GET /api/users/{id}` - Get user
- `PUT /api/users/{id}` - Update user

### Books
- `POST /api/books/` - Add book
- `GET /api/books/` - List/search books
- `GET /api/books/{id}` - Get book
- `PUT /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book

### Loans
- `POST /api/loans/` - Create loan
- `POST /api/loans/{id}/return` - Return book
- `PUT /api/loans/{id}/extend` - Extend loan
- `GET /api/loans/overdue` - List overdue

### Statistics
- `GET /api/statistics/overview` - System stats
- `GET /api/statistics/popular-books` - Popular books
- `GET /api/statistics/active-users` - Active users

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/api/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com", "role": "student"}'
```

### Add a Book
```bash
curl -X POST "http://localhost:8000/api/books/" \
     -H "Content-Type: application/json" \
     -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "978-0-7432-7356-5", "copies": 3}'
```

### Create a Loan
```bash
curl -X POST "http://localhost:8000/api/loans/" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "book_id": 1, "due_date": "2024-02-15T10:00:00"}'
```

## Development

**Run Tests**
```bash
pytest
```

**Project Structure**
```
app/
├── main.py           # FastAPI app
├── config/           # Settings & DB
├── core/             # Middleware & exceptions
├── shared/           # Base models & repos
├── modules/          # Feature modules
│   ├── users/
│   ├── books/
│   ├── loans/
│   └── statistics/
└── api/              # API routing
```

**Architecture**
- Clean Architecture: Controllers → Services → Repositories
- Dependency Injection with FastAPI
- SQLAlchemy ORM with relationship mapping
- Pydantic for validation and serialization
- Comprehensive error handling
- Type hints throughout

## Docker Deployment

```bash
cd docker
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5433
- FastAPI application on port 8000
- Nginx proxy on port 80

## Database Schema

### Users Table
- id, name, email (unique), role, created_at, updated_at

### Books Table  
- id, title, author, isbn (unique), genre, copies, available_copies, created_at, updated_at

### Loans Table
- id, user_id (FK), book_id (FK), issue_date, due_date, return_date, status, extensions_count, created_at, updated_at

## Features

✅ **Complete CRUD Operations**
✅ **Input Validation** 
✅ **Error Handling**
✅ **Database Relationships**
✅ **Search & Filtering**
✅ **Loan Management**
✅ **Statistics & Reports**
✅ **API Documentation**
✅ **Docker Support**
✅ **Test Suite**
✅ **Production Ready**
