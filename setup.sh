#!/bin/bash

set -e

echo "Checking Python version..."
if ! python3 -c 'import sys; exit(not (sys.version_info >= (3,10)))' 2>/dev/null; then
  echo "Python 3.10+ is required. Please install it from https://www.python.org/downloads/"
  exit 1
fi

# 2. Setup venv
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    
    # Create and activate virtual environment
    python3 -m venv .venv
else
    echo "Virtual environment .venv already exists."
fi    
# Activate existing virtual environment
source ./.venv/bin/activate

# 3. Install MCP & requirements
echo "Installing dependencies..."
if ! command -v uv &> /dev/null; then
    echo "uv not found, installing..."
    
    # Install Homebrew if not already installed
    if ! command -v brew >/dev/null 2>&1; then
        echo "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Add Homebrew to PATH
        if [[ $(uname -m) == "arm64" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.bash_profile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
    else
        echo "Homebrew is already installed."
    fi

    echo "Installing uv with Homebrew..."
    brew install uv
    echo ""
else
    echo "uv is already installed."
fi

uv add "mcp[cli]" httpx requests

# 5. Run the access code script
python3 scripts/get_access_token.py

# 5. Run the script to create vectorDB for equity instrument keys
python3 scripts/create_equity_collection.py

# 6. Run the MCP server
echo "Starting MCP server..."
mcp install --with requests --with pandas==2.2.3 --with tqdm --with sentence_transformers --with pymilvus main.py -f .env

echo "MCP server started. Restart the Claude app now."