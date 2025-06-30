#!/usr/bin/env python3
"""
Comprehensive example showing all Akash Python SDK capabilities.

This example demonstrates:
1. Basic REST API usage
2. Advanced async client with gRPC
3. Transaction signing and blockchain interaction
4. Error handling and feature detection
"""

import asyncio
import json

from akash_api import (
    AkashClient, AkashClientError,
    get_available_features, install_instructions,
    ASYNC_AVAILABLE, GRPC_AVAILABLE, TRANSACTION_AVAILABLE
)

# Conditionally import advanced features
if ASYNC_AVAILABLE:
    from akash_api import AkashAsyncClient, create_async_client

if GRPC_AVAILABLE:
    from akash_api import AkashGrpcClient, SyncGrpcWrapper

if TRANSACTION_AVAILABLE:
    from akash_api import create_wallet_from_private_key, AkashTransactionSigner


def basic_rest_example():
    """Example using the basic REST client."""
    print("=== Basic REST Client Example ===")
    
    try:
        # Create client
        client = AkashClient("https://api.akash.network")
        
        print("✓ Client created successfully")
        
        # Check health
        if client.health_check():
            print("✓ API endpoint is healthy")
        else:
            print("⚠ API endpoint health check failed")
            return
        
        # Query deployments
        print("\n📋 Querying deployments...")
        deployments = client.get_deployments()
        print(f"Found {len(deployments.get('deployments', []))} deployments")
        
        # Query providers
        print("\n🏢 Querying providers...")
        providers = client.get_providers()
        print(f"Found {len(providers.get('providers', []))} providers")
        
        # Query market data
        print("\n💰 Querying market data...")
        bids = client.get_bids()
        print(f"Found {len(bids.get('bids', []))} bids")
        
        leases = client.get_leases()
        print(f"Found {len(leases.get('leases', []))} leases")
        
        print("✓ Basic REST example completed successfully")
        
    except AkashClientError as e:
        print(f"✗ Akash client error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


async def advanced_async_example():
    """Example using the advanced async client with all features."""
    print("\n=== Advanced Async Client Example ===")
    
    if not ASYNC_AVAILABLE:
        print("⚠ Async support not available. Install with: pip install aiohttp")
        return
    
    try:
        # Create comprehensive async client
        async with AkashAsyncClient(
            rest_endpoint="https://api.akash.network",
            grpc_endpoint="grpc.akash.network:9090" if GRPC_AVAILABLE else None,
            rpc_endpoint="https://rpc.akash.network" if TRANSACTION_AVAILABLE else None,
            chain_id="akashnet-2"
        ) as client:
            
            print("✓ Async client created with context manager")
            
            # Health check
            health = await client.health_check()
            print(f"Health status: {health}")
            
            # Async REST queries
            print("\n📋 Async REST queries...")
            deployments = await client.get_deployments()
            print(f"Deployments: {len(deployments.get('deployments', []))}")
            
            providers = await client.get_providers()
            print(f"Providers: {len(providers.get('providers', []))}")
            
            print("✓ Advanced async example completed")
            
    except Exception as e:
        print(f"✗ Async example error: {e}")


def feature_detection_example():
    """Example showing feature detection and graceful degradation."""
    print("\n=== Feature Detection Example ===")
    
    # Check available features
    features = get_available_features()
    print("Available features:")
    for feature, available in features.items():
        status = "✓" if available else "✗"
        print(f"  {status} {feature}")
    
    # Show installation instructions for missing features
    missing = install_instructions()
    if missing:
        print("\nTo enable missing features:")
        for feature, command in missing.items():
            print(f"  {feature}: {command}")
    else:
        print("\n✓ All features are available!")
    
    # Show feature flags
    print(f"\nFeature flags:")
    print(f"  ASYNC_AVAILABLE: {ASYNC_AVAILABLE}")
    print(f"  GRPC_AVAILABLE: {GRPC_AVAILABLE}")
    print(f"  TRANSACTION_AVAILABLE: {TRANSACTION_AVAILABLE}")


def main():
    """Run all examples."""
    print("🚀 Akash Python SDK Comprehensive Example")
    print("=" * 50)
    
    # Feature detection first
    feature_detection_example()
    
    # Basic REST example (always available)
    basic_rest_example()
    
    # Advanced features (conditional)
    if ASYNC_AVAILABLE:
        asyncio.run(advanced_async_example())
    else:
        print("\n⚠ Skipping async example - aiohttp not installed")
    
    print("\n" + "=" * 50)
    print("🎉 All available examples completed!")
    
    # Show next steps
    print("\n📖 Next steps:")
    print("1. Install missing dependencies for full functionality:")
    missing = install_instructions()
    for feature, command in missing.items():
        print(f"   {command}")
    print("2. Replace example endpoints with your preferred Akash servers")
    print("3. Use your own private keys for transaction signing")
    print("4. Implement proper error handling for production use")


if __name__ == "__main__":
    main()
