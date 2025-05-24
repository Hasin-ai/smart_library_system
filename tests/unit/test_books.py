def test_create_book(client):
    response = client.post("/api/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "123-456-789",
        "genre": "Fiction",
        "copies": 2
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["copies"] == 2
    assert data["available_copies"] == 2

def test_search_books(client):
    # Create a book first
    client.post("/api/books/", json={
        "title": "Searchable Book",
        "author": "Test Author",
        "isbn": "123-456-789",
        "genre": "Fiction"
    })
    
    response = client.get("/api/books/?search=Searchable")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Searchable Book"
