from typing import  Dict, Any

from src.utils.api import get_upstox_url, http_request, get_headers, create_error_response
from src.lib.milvus import MilvusClient
from src.utils.constants import COLLECTION_NAME

client = MilvusClient(COLLECTION_NAME)

async def get_market_price(company_name: str) -> Dict[Any, Any]:
    """
    Get the market price for a particular stock using the upstox API
    Arguments:
        company_name: Name of the company for which stock price is required
    Returns:
        A dictionary containig information about the current market price of a stock
    Raises:
        Exception: If there is any error in getting the market price
    """
    
    try:
        name, instrument_key = client.run_equity_search(company_name)
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Failed to get instrument key"
            )
    try:
        url = get_upstox_url("market-quote/ltp")
        headers = get_headers()
        try:
            market_quote = http_request(url, headers=headers, params={'instrument_key': instrument_key})
        except Exception as e:
            return create_error_response(
                "SERVER_ERROR",
                "Failed to get market quote from upstox"
            )
        return market_quote
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while retrieving market quote"
            )