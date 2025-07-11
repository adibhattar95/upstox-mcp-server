from typing import Dict
from mcp.server.fastmcp import FastMCP

from src.utils.env import SERVER_NAME
from src.tools.portfolio import get_holdings
from src.tools.market_quote import get_market_price
from src.tools.order import place_order
from src.tools.brokerage import get_brokerage_details
from src.tools.profile import (
    get_profile_details, get_user_funds_margin
)
from src.tools.system import list_capabilities

mcp = FastMCP(SERVER_NAME)

@mcp.tool()
async def get_profile_details_tool() -> Dict:
    """
    Get the user profile details from upstox
    Returns:
        A dictionary containig information about user profile details
    Raises:
        Exception: If there is any error in getting the profile details
    """
    return await get_profile_details()

@mcp.tool()
async def get_user_funds_margin_tool() -> Dict:
    """
    Get the user available funds and margin in Upstox account
    Returns:
        A dictionary containig information about user fund and margin details
    Raises:
        Exception: If there is any error in getting the fund details
    """
    return await get_user_funds_margin()

@mcp.tool()
async def get_holdings_tool() -> Dict:
    """
    Get the user holdings from their Upstox account
    Returns:
        A dictionary containig information about user holding details
    Raises:
        Exception: If there is any error in getting the holding details
    """
    return await get_holdings()

@mcp.tool()
async def get_market_price_tool(company_name: str) -> Dict:
    """
    Get the market price for a particular stock using the upstox API
    Arguments:
        company_name: Name of the company for which stock price is required
    Returns:
        A dictionary containig information about the current market price of a stock
    Raises:
        Exception: If there is any error in getting the market price
    """
    return await get_market_price(company_name)

@mcp.tool()
async def place_order_tool(company_name: str, quantity: int, order_type: str) -> Dict:
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
    return await place_order(company_name, quantity, order_type)

@mcp.tool()
async def get_brokerage_details_tool(instrument_key: str, price: float, quantity: int) -> Dict:
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
    return await get_brokerage_details(instrument_key, price, quantity)

@mcp.tool()
async def list_capabilities_tool() -> Dict[str, str]:
    """
    List all capabilities (resources, tools and prompts) available in this server
    Returns:
        A dictionary containig information about available Server Capabilities
    Raises:
        Exception: If there is any error in getting the server capabilities
    """
    return await list_capabilities()