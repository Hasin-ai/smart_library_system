from typing import Dict, Any
from app.clients.base_client import BaseServiceClient
from app.config.settings import settings
from app.core.exceptions import UserNotFoundException
import httpx

class UserServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.USER_SERVICE_URL, settings.SERVICE_TIMEOUT)
    
    async def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user details from User Service"""
        try:
            return await self._make_request(
                method="GET",
                path=f"/api/users/{user_id}",
                service_name="User Service"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise UserNotFoundException(user_id)
            raise
    
    async def check_health(self) -> bool:
        """Check User Service health"""
        try:
            response = await self._make_request(
                method="GET",
                path="/health",
                service_name="User Service"
            )
            return response.get("status") == "healthy"
        except:
            return False
