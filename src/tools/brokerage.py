from typing import  Dict, Any

from src.utils.api import get_upstox_url, http_request, get_headers, create_error_response


async def get_brokerage_details(instrument_key: str, price: float, quantity: int) -> Dict[Any, Any]:
    """
    Get the brokerage charges applicable for a given token and price
    Arguments:
        instrument_key: Name of the company for which stock price is required
        price: Price at which share is to be purchased
        quantity: Number of shares to buy
    Returns:
        A dictionary containig information about the current market price of a stock
    Raises:
        Exception: If there is any error in getting the brokerage details
    """
    
    try:
        url = get_upstox_url("charges/brokerage")
        params = {
            'instrument_token': instrument_key,
            'quantity': quantity,
            'product': 'D',
            'transaction_type': 'BUY',
            'price': price
        }
        headers = get_headers()
        try:
            brokerage_details = http_request(url, headers=headers, params=params)
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get brokerage details from upstox"
            )
        return brokerage_details
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving brokerage details"
            )