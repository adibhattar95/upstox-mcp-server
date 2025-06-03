from typing import  Dict, Any

from src.utils.api import get_upstox_url, http_request, get_headers, create_error_response

async def get_holdings() -> Dict[Any, Any]:
    """
    Get the user holdings from their Upstox account
    Returns:
        A dictionary containig information about user holding details
    Raises:
        Exception: If there is any error in getting the holding details
    """
    try:
        url = get_upstox_url("portfolio/long-term-holdings")
        headers = get_headers()
        try:
            holding_details = http_request(url, headers=headers)
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get holding details from upstox"
            )
        return holding_details
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving holding details."
            )