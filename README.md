# Upstox MCP Server
**MCP Server for interacting with Upstox APIs**

Upstox MCP Server is a lightweight, plugin-based **Model Context Protocol (MCP)** server designed to perform trading and fund analyhsis using Upstox APIs

### Can learn more about repo by going through the deepwiki
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/adibhattar95/upstox-mcp-server)

## Table of Contents
- [Client Prequisites](#-clientt-prerequisites)
- [Getting Started with the Server](#-getting-started)
- [Available Tools](#-available-tools)

## Client Prequisites
If you want to consume the server from Claude AI (Anthropic):
- **Claude Desktop App** installed from [claude.ai](https://claude.ai)
- **Node.js**

## Getting Started with the Server
1. For users having an Upstox Account, go to this url - **https://account.upstox.com/developer/apps#sandbox**, and create a 
    sandbox app. Give a name to the sandbox app. You can set the redirect URL to **http://localhost:8000**
2. Save the API Key and API SECRET to a .env file under these, along with the server name
    ```env
    SERVER_NAME=SERVER_NAME
    UPSTOX_API_KEY=upstox_api_key
    UPSTOX_SECRET_KEY=upstox_secret_key
    ```
3. Download the instrument keys for upstox from here - **https://upstox.com/developer/api-documentation/instruments/#json-files**, and save it a folder for data/.
4. Run the setup.sh shell file to setup the server. This will check server dependencies and also run the access_token script to get the access_token from Upstox. It will open a browser windon, where you have to enter your upstox pin before proceeding to getting the access token. It will also create the collection for getting the right instrument key for getting market prices of stocks.
5. Open Claude (or your custom MCP client) and start exploring the server!

## Available Tools
| Tool Name                        | Description                                            |
|----------------------------------|------------------------------------------------------- |
| get_profile_details_tool         | Get user profile details from Upstox                   |
| get_user_funds_margin_tool       | Get the fund details from Upstox                       |
| get_holdings_tool                | Get the holdings from Upstox                           |
| get_market_price_tool            | Get the current price of a stock                       |
| place_order_tool                 | Place an order on Upstox for a particular stock        |
| get_brokerage_details_tool       | Get the brokerage charges applicable for a given stock |
| list_capabilities_tool           | List all tools available in the server                 |