from typing import  Dict, Any

from src.utils.api import get_upstox_url, http_request, get_headers, create_error_response
from src.lib.milvus import MilvusClient
from src.utils.constants import COLLECTION_NAME

client = MilvusClient(COLLECTION_NAME)

async def place_order(company_name: str, quantity: int, order_type: str) -> Dict[Any, Any]:
    """
    Place a delivery order for a stock given company name, quantity and order type
    Arguments:
        company_name: Name of the company for which stock order is to be placed
        quantity: Number of shares to be purchased
        order_type: Order Type - Market, Limit, StopLoss
    Returns:
        A success message indicating order was placed successfully
    Raises:
        Exception: If there is any error in placing the order
    """
    
    try:
        name, instrument_key = client.run_equity_search(company_name)
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Failed to get instrument key"
            )
    try:
        url = get_upstox_url("order/place")
        headers = get_headers()
        headers['Content-Type'] = 'application/json'
        data = {
            'quantity': quantity,
            'product': 'D',
            'validity': 'DAY',
            'price': 0,
            'tag': 'string',
            'instrument_token': instrument_key,
            'order_type': order_type,
            'transaction_type': 'BUY',
            'disclosed_quantity': 0,
            'trigger_price': 0,
            'is_amo': False
        }
        try:
            place_order = http_request(url, data=data, headers=headers, params={'instrument_key': instrument_key})
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get market quote from upstox"
            )
        return place_order
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving market quote"
            )