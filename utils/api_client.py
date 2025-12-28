import requests
from typing import Dict, Any, Optional
from config.settings import API_BASE_URL, API_TIMEOUT
from utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = API_TIMEOUT / 1000

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to: {url}")
        response = self.session.get(
            url, params=params, headers=headers, timeout=self.timeout
        )
        logger.info(f"Response status: {response.status_code}")
        return response

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to: {url}")
        response = self.session.post(
            url, data=data, json=json, headers=headers, timeout=self.timeout
        )
        logger.info(f"Response status: {response.status_code}")
        return response

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to: {url}")
        response = self.session.put(
            url, data=data, json=json, headers=headers, timeout=self.timeout
        )
        logger.info(f"Response status: {response.status_code}")
        return response

    def delete(
        self, endpoint: str, headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to: {url}")
        response = self.session.delete(url, headers=headers, timeout=self.timeout)
        logger.info(f"Response status: {response.status_code}")
        return response

    def set_auth_token(self, token: str) -> None:
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authorization token set")

    def close(self) -> None:
        self.session.close()
        logger.info("API session closed")
