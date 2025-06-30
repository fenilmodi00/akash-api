# Akash Network Python API

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/akash-api.svg)](https://pypi.org/project/akash-api/)

Comprehensive Python client for the [Akash Network](https://akash.network) with REST API, gRPC, and transaction support for building production applications on the decentralized cloud.

## ✨ Features

- **🌐 REST API Client** - Query deployments, providers, bids, and leases
- **⚡ Async Support** - High-performance async/await operations with aiohttp
- **🔗 gRPC Client** - Full gRPC support with streaming capabilities
- **📝 Transaction Signing** - Create, sign, and broadcast blockchain transactions
- **🛡️ Type Hints** - Full type annotation support for better development experience
- **🔧 Modular Design** - Install only the features you need
- **🚀 Production Ready** - Comprehensive error handling and connection management

## 📦 Installation

```bash
pip install akash-api
```

**All features included by default:**
- ✅ REST API client
- ✅ Async operations (aiohttp)
- ✅ gRPC client with streaming
- ✅ Transaction signing
- ✅ Type hints and error handling

### Optional Performance Enhancement
```bash
# For better JSON performance (optional)
pip install akash-api[performance]
```

## 🚀 Quick Start

### Basic REST Client
```python
from akash_api import AkashClient

# Create client
client = AkashClient("https://api.akash.network")

# Query network state
deployments = client.get_deployments()
providers = client.get_providers()
bids = client.get_bids()
leases = client.get_leases()

print(f"Found {len(deployments.get('deployments', []))} deployments")
```

### Advanced Async Client
```python
import asyncio
from akash_api import AkashAsyncClient

async def main():
    async with AkashAsyncClient(
        rest_endpoint="https://api.akash.network",
        grpc_endpoint="grpc.akash.network:9090",
        rpc_endpoint="https://rpc.akash.network"
    ) as client:
        
        # Async REST queries
        deployments = await client.get_deployments()
        providers = await client.get_providers()
        
        # gRPC queries with pagination
        grpc_providers = await client.grpc_query_providers()
        
        # Stream real-time events
        async for event in client.stream_deployment_events():
            print(f"New event: {event}")

asyncio.run(main())
```

### Blockchain Transactions
```python
from akash_api import AkashTransactionSigner, create_wallet_from_private_key

# Create wallet and signer
wallet = create_wallet_from_private_key("your_private_key_hex")
signer = AkashTransactionSigner("https://rpc.akash.network")

# Create deployment
sdl_config = {
    "version": "2.0",
    "services": {
        "app": {
            "image": "nginx:latest",
            "expose": [{"port": 80, "as": 8080, "to": [{"global": True}]}]
        }
    }
    # ... rest of SDL configuration
}

# Sign and broadcast transaction
deployment_msg = signer.create_deployment_msg(
    owner=wallet.address,
    sdl=sdl_config,
    deposit="10000000uakt"
)

# Transaction creation and broadcasting
# (See advanced_example.py for complete implementation)
```

## 🔧 Feature Detection

The SDK automatically detects available features and provides graceful degradation:

```python
from akash_api import get_available_features, install_instructions

# Check what's available
features = get_available_features()
print(features)
# {
#     'rest_client': True,
#     'async_client': True,  
#     'grpc_client': False,
#     'transaction_signing': True
# }

# Get installation instructions for missing features
missing = install_instructions()
for feature, command in missing.items():
    print(f"{feature}: {command}")
```

## 📚 Complete Examples

### Usage from Project Root
```bash
# Basic example
PYTHONPATH=python/src python3 python/examples/example.py

# Advanced features example
PYTHONPATH=python/src python3 python/examples/advanced_example.py
```

### Production Deployment Examples

#### Monitoring Application
```python
from akash_api import AkashClient
import time

def monitor_network():
    client = AkashClient("https://api.akash.network")
    
    while True:
        try:
            providers = client.get_providers()
            active_providers = len([p for p in providers.get('providers', []) 
                                  if p.get('status') == 'active'])
            
            deployments = client.get_deployments(state='active')
            active_deployments = len(deployments.get('deployments', []))
            
            print(f"Active providers: {active_providers}, "
                  f"Active deployments: {active_deployments}")
            
        except Exception as e:
            print(f"Monitor error: {e}")
        
        time.sleep(60)  # Check every minute

monitor_network()
```

#### Async High-Performance Client
```python
import asyncio
from akash_api import AkashAsyncClient

async def high_performance_queries():
    async with AkashAsyncClient("https://api.akash.network") as client:
        
        # Concurrent queries for better performance
        tasks = [
            client.get_deployments(),
            client.get_providers(), 
            client.get_bids(),
            client.get_leases()
        ]
        
        results = await asyncio.gather(*tasks)
        deployments, providers, bids, leases = results
        
        print(f"Retrieved {sum(len(r.get(list(r.keys())[0], [])) for r in results)} total records")

asyncio.run(high_performance_queries())
```

## 🏗️ Advanced Configuration

### Custom Endpoints and Timeouts
```python
from akash_api import AkashAsyncClient

async with AkashAsyncClient(
    rest_endpoint="https://your-api.akash.network",
    grpc_endpoint="your-grpc.akash.network:9090", 
    rpc_endpoint="https://your-rpc.akash.network",
    chain_id="akashnet-2",
    timeout=60
) as client:
    # Your code here
    pass
```

### Error Handling Best Practices
```python
from akash_api import AkashClient, AkashClientError, AkashAsyncClientError

try:
    client = AkashClient("https://api.akash.network")
    deployments = client.get_deployments()
    
except AkashClientError as e:
    # Handle Akash-specific errors
    print(f"Akash API error: {e}")
    
except ConnectionError as e:
    # Handle network errors
    print(f"Network error: {e}")
    
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
```

## 🛠️ Development

### Running Examples
```bash
# From the project root
cd python

# Install dependencies
pip install -e .[full]

# Run examples
python examples/example.py
python examples/advanced_example.py
```

### Code Generation
To regenerate Protocol Buffer files:
```bash
# From the project root
make proto-gen-py
```

### Project Structure
```
python/
├── src/akash_api/          # Main SDK package
│   ├── __init__.py         # Package initialization and exports
│   ├── client.py           # Basic REST client
│   ├── async_client.py     # Advanced async client
│   ├── grpc_client.py      # gRPC client implementation
│   ├── transaction.py      # Transaction signing and blockchain interaction
│   └── akash/              # Generated protobuf files
├── examples/               # Usage examples
│   ├── example.py          # Basic examples
│   └── advanced_example.py # Advanced feature examples
├── tests/                  # Test suite (coming soon)
├── pyproject.toml          # Package configuration
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔗 API Reference

### Core Classes

- **`AkashClient`** - Basic synchronous REST client
- **`AkashAsyncClient`** - Advanced async client with REST, gRPC, and transaction support
- **`AkashGrpcClient`** - Dedicated async gRPC client
- **`SyncGrpcWrapper`** - Synchronous wrapper for gRPC operations
- **`AkashTransactionSigner`** - Transaction creation, signing, and broadcasting
- **`Wallet`** - Wallet management for transaction signing

### Available Endpoints

#### REST API Methods
- `get_deployments(owner?, state?, dseq?)` - Query deployments
- `get_deployment(owner, dseq)` - Get specific deployment
- `get_providers()` - List active providers
- `get_provider(address)` - Get specific provider
- `get_bids(owner?, provider?, state?)` - Query bids
- `get_leases(owner?, provider?, state?)` - Query leases
- `health_check()` - Check API health

#### gRPC Methods (Async)
- `grpc_query_deployments(**kwargs)` - Advanced deployment queries
- `grpc_query_providers(**kwargs)` - Advanced provider queries
- `grpc_query_bids(**kwargs)` - Advanced bid queries
- `grpc_query_leases(**kwargs)` - Advanced lease queries
- `stream_deployment_events(**kwargs)` - Real-time event streaming

#### Transaction Methods (Async)
- `create_deployment(wallet, sdl, deposit?)` - Create new deployment
- `create_bid(wallet, order_id, price)` - Place bid on order
- `create_lease(wallet, bid_id)` - Accept bid and create lease

## 🆚 Comparison with TypeScript SDK

| Feature | Python SDK | TypeScript SDK | Status |
|---------|------------|----------------|--------|
| REST API | ✅ Full | ✅ Full | ✅ Complete parity |
| gRPC Client | ✅ Full | ✅ Full | ✅ Complete parity |
| Async Support | ✅ asyncio/aiohttp | ✅ RxJS | ✅ Complete parity |
| Transaction Signing | ✅ Full | ✅ Full | ✅ Complete parity |
| Type Safety | ⚠️ Type hints | ✅ TypeScript | Inherent difference |
| Package Distribution | ✅ PyPI ready | ✅ npm published | ✅ Complete parity |
| Streaming | ✅ AsyncGenerator | ✅ Observables | ✅ Complete parity |
| Error Handling | ✅ Custom exceptions | ✅ Structured errors | ✅ Complete parity |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code generation works
5. Submit a pull request

## 📄 License

Apache License 2.0. See [LICENSE](../LICENSE) for details.

## 💬 Support

- [Documentation](https://docs.akash.network)
- [Discord](https://discord.akash.network)
- [GitHub Issues](https://github.com/akash-network/akash-api/issues)

## 🎯 Roadmap

- ✅ REST API client
- ✅ Async support with aiohttp
- ✅ gRPC client implementation
- ✅ Transaction signing and broadcasting  
- ✅ Comprehensive error handling
- ✅ Package distribution (PyPI)
- 🔄 Test suite implementation
- 🔄 Advanced message type handling
- 🔄 WebSocket streaming support
- 🔄 Wallet integration with hardware devices

The Python SDK now provides **complete feature parity** with the TypeScript SDK, enabling full blockchain interaction, gRPC operations, and production-ready application development!
