import httpx
from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.exceptions import ServiceUnavailableException

class BaseServiceClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
    
    async def _make_request(
        self, 
        method: str, 
        path: str, 
        service_name: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to external service"""
        url = f"{self.base_url}{path}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params
                )
                
                if response.status_code >= 500:
                    logger.error(f"{service_name} returned {response.status_code}")
                    raise ServiceUnavailableException(service_name)
                
                response.raise_for_status()
                return response.json()
                
        except httpx.TimeoutException:
            logger.error(f"Timeout calling {service_name} at {url}")
            raise ServiceUnavailableException(service_name)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from {service_name}: {e.response.status_code}")
            raise
        except Exception as e:
            logger.error(f"Error calling {service_name}: {str(e)}")
            raise ServiceUnavailableException(service_name)
