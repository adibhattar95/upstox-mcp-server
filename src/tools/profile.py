from typing import  Dict, Any

from src.utils.api import get_upstox_url, http_request, get_headers, create_error_response

async def get_profile_details() -> Dict[Any, Any]:
    """
    Get the user profile details from upstox
    Returns:
        A dictionary containig information about user profile details
    Raises:
        Exception: If there is any error in getting the profile details
    """
    try:
        url = get_upstox_url("user/profile")
        headers = get_headers()
        try:
            profile_details = http_request(url, headers=headers)
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get profile details from upstox"
            )
        return profile_details
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving profile details."
            )
    
async def get_user_funds_margin() -> Dict[Any, Any]:
    """
    Get the user available funds and margin in Upstox account
    Returns:
        A dictionary containig information about user fund and margin details
    Raises:
        Exception: If there is any error in getting the fund details
    """
    try:
        url = get_upstox_url("user/get-funds-and-margin")
        headers = get_headers()
        try:
            fund_details = http_request(url, headers=headers)
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get fund details from upstox"
            )
        return fund_details
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving fund details."
            )

