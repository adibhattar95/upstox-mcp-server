from typing import Dict

from src.utils.env import SERVER_NAME
from src.utils.api import create_error_response

async def list_capabilities() -> Dict[str, str]:
    """
    List all capabilities (resources, tools and prompts) available in this server
    Returns:
        A dictionary containig information about available Server Capabilities
    Raises:
        Exception: If there is any error in getting the server capabilities
    """
    try:
        capabilities = {
            "server_name": SERVER_NAME,
            "tools": [
                {
                    "name": "get_profile_details_tool",
                    "description": "Get the user profile details from upstox",
                    "parameters": None
                },
                {
                    "name": "get_user_funds_margin_tool",
                    "description": "et the user available funds and margin in Upstox account",
                    "parameters": None
                },
                {
                    "name": "get_holdings_tool",
                    "description": "Get the user holdings from their Upstox account",
                    "parameters": None
                },
                {
                    "name": "get_market_price_tool",
                    "description": "Get the market price for the given company",
                    "parameters": ["company_name"]
                },
                {
                    "name": "place_order_tool",
                    "description": "Place an order for a stock given company name, quantity and order type",
                    "parameters": ["company_name", "quantity", "order_type"]
                }
            ],
            "example_usage": [
                "get_profile_details_tool()",
                "get_user_funds_margin_tool()",
                "get_holdings_tool()",
                "get_market_price_tool('Reliance')",
                "place_order_tool('Reliance', 10, Market)"
            ]
        }
        return capabilities
    except Exception as e:
        return create_error_response(
                "SERVER_ERROR",
                "Unexpected error occurred while listing capabilities."
            )

