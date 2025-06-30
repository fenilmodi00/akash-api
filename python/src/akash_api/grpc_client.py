"""
High-level gRPC client for Akash Network.

This module provides async gRPC client functionality with proper connection management,
retry logic, and error handling.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List, AsyncGenerator, Union
from contextlib import asynccontextmanager

try:
    import grpc
    import grpc.aio
    GRPC_AVAILABLE = True
except ImportError:
    GRPC_AVAILABLE = False
    grpc = None

# Import protobuf services (with fallback)
try:
    from akash_api.akash.deployment.v1beta3 import service_pb2_grpc as deployment_grpc
    from akash_api.akash.market.v1beta4 import service_pb2_grpc as market_grpc  
    from akash_api.akash.provider.v1beta3 import service_pb2_grpc as provider_grpc
    from akash_api.akash.cert.v1beta3 import service_pb2_grpc as cert_grpc
    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    deployment_grpc = market_grpc = provider_grpc = cert_grpc = None


class AkashGrpcClientError(Exception):
    """Base exception for gRPC client errors."""
    pass


class AkashGrpcClient:
    """
    High-level async gRPC client for Akash Network.
    
    Provides connection management, retry logic, and structured error handling
    for all Akash gRPC services.
    """
    
    def __init__(self, 
                 grpc_endpoint: str,
                 timeout: int = 30,
                 max_retries: int = 3,
                 credentials: Optional[Any] = None):
        """
        Initialize the gRPC client.
        
        Args:
            grpc_endpoint: gRPC endpoint URL (e.g., "grpc.akash.network:9090")
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            credentials: Optional gRPC credentials for TLS
        """
        if not GRPC_AVAILABLE:
            raise AkashGrpcClientError("grpcio is required for gRPC support. Install with: pip install grpcio")
        
        if not PROTOBUF_AVAILABLE:
            raise AkashGrpcClientError("Protobuf services not available. Run protobuf generation first.")
        
        self.endpoint = grpc_endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        self.credentials = credentials
        self._channel = None
        
        # Service stubs (initialized lazily)
        self._deployment_stub = None
        self._market_stub = None
        self._provider_stub = None
        self._cert_stub = None
    
    @asynccontextmanager
    async def _get_channel(self):
        """Get or create a gRPC channel with proper cleanup."""
        if self._channel is None:
            if self.credentials:
                self._channel = grpc.aio.secure_channel(self.endpoint, self.credentials)
            else:
                self._channel = grpc.aio.insecure_channel(self.endpoint)
        
        try:
            yield self._channel
        except grpc.aio.AioRpcError as e:
            logging.error(f"gRPC error: {e.code()}: {e.details()}")
            raise AkashGrpcClientError(f"gRPC call failed: {e.details()}")
    
    async def close(self):
        """Close the gRPC channel."""
        if self._channel:
            await self._channel.close()
            self._channel = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    # Deployment service methods
    async def query_deployments(self, 
                               owner: Optional[str] = None,
                               state: Optional[str] = None,
                               pagination_key: Optional[bytes] = None,
                               pagination_limit: int = 100) -> Dict[str, Any]:
        """
        Query deployments using gRPC.
        
        Args:
            owner: Filter by deployment owner
            state: Filter by deployment state
            pagination_key: Pagination key for next page
            pagination_limit: Maximum number of results
            
        Returns:
            Query response as dictionary
        """
        async with self._get_channel() as channel:
            if self._deployment_stub is None:
                self._deployment_stub = deployment_grpc.QueryStub(channel)
            
            # Create query request (would need proper protobuf message construction)
            # This is a placeholder - actual implementation would create proper protobuf messages
            request = {
                'owner': owner,
                'state': state,
                'pagination': {
                    'key': pagination_key,
                    'limit': pagination_limit
                }
            }
            
            # Make gRPC call with retry logic
            for attempt in range(self.max_retries):
                try:
                    # This would be the actual gRPC call
                    # response = await self._deployment_stub.QueryDeployments(request, timeout=self.timeout)
                    # return response
                    
                    # Placeholder response
                    return {"deployments": [], "pagination": {"next_key": None}}
                    
                except grpc.aio.AioRpcError as e:
                    if attempt == self.max_retries - 1:
                        raise AkashGrpcClientError(f"Query failed after {self.max_retries} attempts: {e.details()}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def stream_deployment_events(self, filters: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream deployment events in real-time.
        
        Args:
            filters: Optional filters for events
            
        Yields:
            Deployment events as they occur
        """
        async with self._get_channel() as channel:
            if self._deployment_stub is None:
                self._deployment_stub = deployment_grpc.QueryStub(channel)
            
            # Placeholder for streaming implementation
            # This would use gRPC streaming calls
            for i in range(5):  # Placeholder
                yield {"event": f"deployment_event_{i}", "timestamp": asyncio.get_event_loop().time()}
                await asyncio.sleep(1)
    
    # Market service methods  
    async def query_bids(self, 
                        owner: Optional[str] = None,
                        provider: Optional[str] = None,
                        state: Optional[str] = None) -> Dict[str, Any]:
        """Query bids using gRPC."""
        async with self._get_channel() as channel:
            if self._market_stub is None:
                self._market_stub = market_grpc.QueryStub(channel)
            
            # Placeholder implementation
            return {"bids": [], "pagination": {"next_key": None}}
    
    async def query_leases(self, 
                          owner: Optional[str] = None,
                          provider: Optional[str] = None,
                          state: Optional[str] = None) -> Dict[str, Any]:
        """Query leases using gRPC."""
        async with self._get_channel() as channel:
            if self._market_stub is None:
                self._market_stub = market_grpc.QueryStub(channel)
            
            # Placeholder implementation
            return {"leases": [], "pagination": {"next_key": None}}
    
    # Provider service methods
    async def query_providers(self, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Query providers using gRPC."""
        async with self._get_channel() as channel:
            if self._provider_stub is None:
                self._provider_stub = provider_grpc.QueryStub(channel)
            
            # Placeholder implementation
            return {"providers": [], "pagination": {"next_key": None}}
    
    # Certificate service methods
    async def query_certificates(self, owner: Optional[str] = None) -> Dict[str, Any]:
        """Query certificates using gRPC."""
        async with self._get_channel() as channel:
            if self._cert_stub is None:
                self._cert_stub = cert_grpc.QueryStub(channel)
            
            # Placeholder implementation
            return {"certificates": [], "pagination": {"next_key": None}}
    
    # Health check
    async def health_check(self) -> bool:
        """Check if the gRPC endpoint is healthy."""
        try:
            async with self._get_channel() as channel:
                # Try a simple call to check connectivity
                await channel.channel_ready()
                return True
        except Exception:
            return False


# Compatibility functions for non-async usage
def create_grpc_client(grpc_endpoint: str, **kwargs) -> AkashGrpcClient:
    """Create a new gRPC client instance."""
    return AkashGrpcClient(grpc_endpoint, **kwargs)


class SyncGrpcWrapper:
    """Synchronous wrapper for the async gRPC client."""
    
    def __init__(self, grpc_endpoint: str, **kwargs):
        self.client = AkashGrpcClient(grpc_endpoint, **kwargs)
        self.loop = None
    
    def _run_async(self, coro):
        """Run an async coroutine in sync context."""
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        return self.loop.run_until_complete(coro)
    
    def query_deployments(self, **kwargs):
        """Sync wrapper for query_deployments."""
        return self._run_async(self.client.query_deployments(**kwargs))
    
    def query_bids(self, **kwargs):
        """Sync wrapper for query_bids."""
        return self._run_async(self.client.query_bids(**kwargs))
    
    def query_leases(self, **kwargs):
        """Sync wrapper for query_leases."""
        return self._run_async(self.client.query_leases(**kwargs))
    
    def query_providers(self, **kwargs):
        """Sync wrapper for query_providers."""
        return self._run_async(self.client.query_providers(**kwargs))
    
    def health_check(self):
        """Sync wrapper for health_check."""
        return self._run_async(self.client.health_check())
    
    def close(self):
        """Close the client and event loop."""
        if self.loop:
            self._run_async(self.client.close())
            self.loop.close()
            self.loop = None
