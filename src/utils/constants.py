UPSTOX_BASE_URL="https://api.upstox.com/v2/"
DEFAULT_TIMEOUT=30
MILVUS_HOST='127.0.0.1'
MILVUS_PORT='19530'
COLLECTION_NAME='equity_stock_symbols'

ERROR_CODES = {
    "VALIDATION_ERROR": 400,
    "AUTHETICATION_ERROR": 401,
    "AUTHORIZATION_ERROR": 403,
    "RESOURCE_NOT_FOUND": 404,
    "TIMEOUT_ERROR": 408,
    "CONFLICT_ERROR": 409,
    "RATE_LIMIT_ERROR": 429,
    "SERVER_ERROR": 500,
    "SERVICE_UNAVAILABLE": 503
}