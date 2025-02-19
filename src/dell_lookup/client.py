from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ValidationError
import httpx


class DellWarrantyClient:
    """
    A Python client for interacting with the Dell Warranty API using HTTPX.

    Attributes:
        client_id (str): The Client ID for authentication.
        client_secret (str): The Client Secret for authentication.
        base_url (str): The base URL for the API endpoints.
        token (str): The Bearer token for authorization.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initializes the DellWarrantyClient and authenticates with the Dell Warranty API.

        Args:
            client_id (str): The Client ID for API access.
            client_secret (str): The Client Secret for API access.

        Raises:
            httpx.HTTPError: If the authentication request fails.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://apigtwb2c.us.dell.com/PROD/sbil/eapi/v5"
        self.token = self._authenticate()

    def _authenticate(self) -> str:
        """
        Authenticates with the Dell Warranty API to obtain a Bearer token.

        Returns:
            str: The Bearer token.

        Raises:
            httpx.HTTPError: If the authentication request fails.
        """
        auth_url = "https://apigtwb2c.us.dell.com/auth/oauth/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        with httpx.Client() as client:
            response = client.post(auth_url, headers=headers, data=payload)
            try:
                response.raise_for_status()  # Raise exception for HTTP errors
            except httpx.HTTPStatusError as e:
                print(f"Error: {e.response.text}")  # Log the response content
                raise  # Re-raise the exception
            token = response.json().get("access_token")
            if not token:
                raise ValueError("Failed to retrieve access token.")
            return token

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Makes a GET request to the Dell Warranty API.

        Args:
            endpoint (str): The API endpoint to query.
            params (Dict[str, Any]): The query parameters.

        Returns:
            Dict[str, Any]: The parsed JSON response.

        Raises:
            httpx.HTTPError: If the HTTP request fails.
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}

        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    def get_asset_header(self, service_tags: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches asset header details.

        Args:
            service_tags (List[str]): A list of service tags (up to 100).

        Returns:
            List[Dict[str, Any]]: A list of asset header details.
        """
        params = {"servicetags": ",".join(service_tags)}
        return self._make_request("assets", params)

    def get_asset_warranty(self, service_tags: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches asset warranty details.

        Args:
            service_tags (List[str]): A list of service tags (up to 100).

        Returns:
            List[Dict[str, Any]]: A list of asset warranty details.
        """
        params = {"servicetags": ",".join(service_tags)}
        return self._make_request("asset-entitlements", params)

    def get_asset_details(self, service_tag: str) -> Dict[str, Any]:
        """
        Fetches detailed asset information.

        Args:
            service_tag (str): A single service tag.

        Returns:
            Dict[str, Any]: Asset details.
        """
        params = {"servicetag": service_tag}
        return self._make_request("asset-components", params)

    def get_asset_summary(self, service_tag: str) -> Dict[str, Any]:
        """
        Fetches summary details for an asset.

        Args:
            service_tag (str): A single service tag.

        Returns:
            Dict[str, Any]: Asset summary details.
        """
        params = {"servicetag": service_tag}
        return self._make_request("asset-entitlement-components", params)


# Example Pydantic models for validation
class AssetHeader(BaseModel):
    id: int
    serviceTag: str
    orderBuid: Optional[int]
    shipDate: Optional[str]
    productCode: Optional[str]
    localChannel: Optional[str]
    productLineDescription: Optional[str]
    productFamily: Optional[str]
    systemDescription: Optional[str]
    productLobDescription: Optional[str]
    countryCode: Optional[str]
    duplicated: Optional[bool]
    invalid: Optional[bool]