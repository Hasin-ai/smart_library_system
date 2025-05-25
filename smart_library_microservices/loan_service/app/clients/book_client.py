from typing import Dict, Any
from app.clients.base_client import BaseServiceClient
from app.config.settings import settings
from app.core.exceptions import BookNotFoundException, BookNotAvailableException
import httpx

class BookServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.BOOK_SERVICE_URL, settings.SERVICE_TIMEOUT)
    
    async def get_book(self, book_id: int) -> Dict[str, Any]:
        """Get book details from Book Service"""
        try:
            return await self._make_request(
                method="GET",
                path=f"/api/books/{book_id}",
                service_name="Book Service"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise BookNotFoundException(book_id)
            raise
    
    async def update_availability(self, book_id: int, operation: str) -> Dict[str, Any]:
        """Update book availability in Book Service"""
        try:
            return await self._make_request(
                method="PATCH",
                path=f"/api/books/{book_id}/availability",
                service_name="Book Service",
                data={"operation": operation}
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                raise BookNotAvailableException(book_id)
            elif e.response.status_code == 404:
                raise BookNotFoundException(book_id)
            raise
    
    async def check_health(self) -> bool:
        """Check Book Service health"""
        try:
            response = await self._make_request(
                method="GET",
                path="/health",
                service_name="Book Service"
            )
            return response.get("status") == "healthy"
        except:
            return False
