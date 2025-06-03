from typing import Optional, Dict, Any, Union, Tuple, IO
import requests
from requests.exceptions import HTTPError

from src.utils.constants import UPSTOX_BASE_URL, DEFAULT_TIMEOUT, ERROR_CODES
from src.utils.env import UPSTOX_ACCESS_TOKEN

def get_upstox_url(path: str) -> str:
    return UPSTOX_BASE_URL + path

def http_request(url: str,
                 method: str = 'GET',
                 params: Optional[Dict[str, Optional[Union[str, int, float]]]] = None,
                 data: Optional[Any] = None,
                 files: Optional[Dict[str, Tuple[str, IO[Any], str]]] = None,
                 headers: Optional[Dict[str, str]] = None
                 ) -> Any:
    """
    Make an http request and return the json response
    """
    try:
        response = requests.request(method=method, url=url, params=params, json=data, files=files,
                                    headers=headers, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        error_message = e.response.text
        raise ValueError(f"API request failed: {e.response.status_code} - {error_message}")
    
def create_error_response(code_key: str, message: str, details: Dict[Any, Any] | None = None) -> Dict:
    code = ERROR_CODES.get(code_key, 500)
    safe_details = {}
    if details:
        for key, value in details.items():
            if key in ['field', 'resource', 'error_type']:
                safe_details[key] = str(value)
    return {
        "error": {
            "code": code,
            "code_key": code_key,
            "message": message,
            "details": safe_details
        }
    }

def get_headers() -> Dict:
    return {
        'Authorization': f"Bearer {UPSTOX_ACCESS_TOKEN}",
        'Accept': 'application/json'
    }