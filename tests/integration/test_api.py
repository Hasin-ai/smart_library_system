def test_full_workflow(client):
    # Create user
    user_response = client.post("/api/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "role": "student"
    })
    user_id = user_response.json()["id"]
    
    # Create book
    book_response = client.post("/api/books/", json={
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "123-456-789",
        "copies": 1
    })
    book_id = book_response.json()["id"]
    
    # Create loan
    from datetime import datetime, timedelta
    due_date = (datetime.now() + timedelta(days=14)).isoformat()
    
    loan_response = client.post("/api/loans/", json={
        "user_id": user_id,
        "book_id": book_id,
        "due_date": due_date
    })
    assert loan_response.status_code == 201
    loan_id = loan_response.json()["id"]
    
    # Check book availability decreased
    book_check = client.get(f"/api/books/{book_id}")
    assert book_check.json()["available_copies"] == 0
    
    # Return loan
    return_response = client.post(f"/api/loans/{loan_id}/return")
    assert return_response.status_code == 200
    
    # Check book availability increased
    book_final = client.get(f"/api/books/{book_id}")
    assert book_final.json()["available_copies"] == 1
