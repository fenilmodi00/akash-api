"""
Akash Network API client for Python

This package provides comprehensive access to the Akash Network including:
- REST API client for queries and monitoring
- gRPC client for advanced operations and streaming
- Transaction signing and blockchain interaction
- Async support for high-performance applications

Example usage:

    # Simple REST client
    from akash_api import AkashClient
    client = AkashClient("https://api.akash.network")
    deployments = client.get_deployments()

    # Advanced async client with full features
    from akash_api import AkashAsyncClient, create_wallet_from_private_key
    
    async with AkashAsyncClient(
        rest_endpoint="https://api.akash.network",
        grpc_endpoint="grpc.akash.network:9090",
        rpc_endpoint="https://rpc.akash.network"
    ) as client:
        # Query via REST
        deployments = await client.get_deployments()
        
        # Query via gRPC
        providers = await client.grpc_query_providers()
        
        # Create blockchain transactions
        wallet = create_wallet_from_private_key("your_private_key_hex")
        result = await client.create_deployment(wallet, sdl_config)

    # Transaction signing only
    from akash_api import AkashTransactionSigner, Wallet
    signer = AkashTransactionSigner("https://rpc.akash.network")
    wallet = Wallet.from_private_key("your_private_key_hex")
"""

__version__ = "0.2.0"

# Core clients
from akash_api.client import AkashClient, AkashClientError

# Advanced clients (all included by default)
from akash_api.async_client import AkashAsyncClient, AkashAsyncClientError, create_async_client
from akash_api.grpc_client import AkashGrpcClient, AkashGrpcClientError, SyncGrpcWrapper, create_grpc_client
from akash_api.transaction import (
    AkashTransactionSigner, AkashTransactionError,
    Wallet, TransactionInfo,
    create_wallet_from_private_key, create_signer
)

# Feature availability (all True by default)
ASYNC_AVAILABLE = True
GRPC_AVAILABLE = True
TRANSACTION_AVAILABLE = True

# Always available (all features included by default)
__all__ = [
    # Core
    "AkashClient", 
    "AkashClientError",
    
    # Feature availability flags
    "ASYNC_AVAILABLE",
    "GRPC_AVAILABLE", 
    "TRANSACTION_AVAILABLE",
    
    # Async client
    "AkashAsyncClient",
    "AkashAsyncClientError", 
    "create_async_client",
    
    # gRPC client
    "AkashGrpcClient",
    "AkashGrpcClientError",
    "SyncGrpcWrapper",
    "create_grpc_client",
    
    # Transaction support
    "AkashTransactionSigner",
    "AkashTransactionError",
    "Wallet",
    "TransactionInfo", 
    "create_wallet_from_private_key",
    "create_signer",
]


def get_available_features():
    """
    Get a list of available features.
    
    Returns:
        Dict with feature availability (all True by default)
    """
    return {
        "rest_client": True,
        "async_client": True,
        "grpc_client": True,
        "transaction_signing": True,
    }


def install_instructions():
    """
    Get installation instructions.
    
    Returns:
        Dict with installation info (all features included by default)
    """
    return {
        "message": "All features are included! Install with: pip install akash-api",
        "optional": {
            "performance": "pip install akash-api[performance]  # Better JSON performance"
        }
    }
