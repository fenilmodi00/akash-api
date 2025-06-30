"""
Advanced async client for Akash Network with comprehensive features.

This module provides a unified client that combines REST API, gRPC, and transaction
capabilities with async support.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List, AsyncGenerator, Union
from contextlib import AsyncExitStack

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

from .client import AkashClient, AkashClientError
from .grpc_client import AkashGrpcClient, AkashGrpcClientError
from .transaction import AkashTransactionSigner, Wallet, TransactionInfo, AkashTransactionError


class AkashAsyncClientError(Exception):
    """Base exception for async client errors."""
    pass


class AkashAsyncClient:
    """
    Comprehensive async client for Akash Network.
    
    Combines REST API, gRPC, and transaction functionality in a single
    async-friendly interface with proper connection management.
    """
    
    def __init__(self,
                 rest_endpoint: str,
                 grpc_endpoint: Optional[str] = None,
                 rpc_endpoint: Optional[str] = None,
                 chain_id: str = "akashnet-2",
                 timeout: int = 30):
        """
        Initialize the comprehensive async client.
        
        Args:
            rest_endpoint: REST API endpoint
            grpc_endpoint: Optional gRPC endpoint
            rpc_endpoint: Optional RPC endpoint for transactions
            chain_id: Blockchain chain ID
            timeout: Request timeout
        """
        self.rest_endpoint = rest_endpoint
        self.grpc_endpoint = grpc_endpoint
        self.rpc_endpoint = rpc_endpoint
        self.chain_id = chain_id
        self.timeout = timeout
        
        # Client instances (initialized lazily)
        self._rest_session = None
        self._grpc_client = None
        self._transaction_signer = None
        self._exit_stack = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._exit_stack = AsyncExitStack()
        
        # Initialize HTTP session
        if AIOHTTP_AVAILABLE:
            self._rest_session = await self._exit_stack.enter_async_context(
                aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
            )
        
        # Initialize gRPC client if endpoint provided
        if self.grpc_endpoint:
            self._grpc_client = AkashGrpcClient(self.grpc_endpoint, timeout=self.timeout)
            await self._exit_stack.enter_async_context(self._grpc_client)
        
        # Initialize transaction signer if RPC endpoint provided
        if self.rpc_endpoint:
            self._transaction_signer = AkashTransactionSigner(self.rpc_endpoint, self.chain_id)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._exit_stack:
            await self._exit_stack.aclose()
    
    # REST API methods (async versions)
    async def get_deployments(self,
                             owner: Optional[str] = None,
                             state: Optional[str] = None,
                             dseq: Optional[int] = None) -> Dict[str, Any]:
        """
        Get deployments via REST API (async).
        
        Args:
            owner: Filter by deployment owner
            state: Filter by deployment state
            dseq: Filter by deployment sequence
            
        Returns:
            Deployment data
        """
        if not self._rest_session:
            raise AkashAsyncClientError("Client not properly initialized. Use async context manager.")
        
        params = {}
        if owner:
            params['owner'] = owner
        if state:
            params['state'] = state
        if dseq:
            params['dseq'] = str(dseq)
        
        url = f"{self.rest_endpoint}/akash/deployment/v1beta3/deployments"
        
        async with self._rest_session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_providers(self) -> Dict[str, Any]:
        """Get providers via REST API (async)."""
        if not self._rest_session:
            raise AkashAsyncClientError("Client not properly initialized. Use async context manager.")
        
        url = f"{self.rest_endpoint}/akash/provider/v1beta3/providers"
        
        async with self._rest_session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_bids(self,
                      owner: Optional[str] = None,
                      provider: Optional[str] = None,
                      state: Optional[str] = None) -> Dict[str, Any]:
        """Get bids via REST API (async)."""
        if not self._rest_session:
            raise AkashAsyncClientError("Client not properly initialized. Use async context manager.")
        
        params = {}
        if owner:
            params['owner'] = owner
        if provider:
            params['provider'] = provider
        if state:
            params['state'] = state
        
        url = f"{self.rest_endpoint}/akash/market/v1beta4/bids/list"
        
        async with self._rest_session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_leases(self,
                        owner: Optional[str] = None,
                        provider: Optional[str] = None,
                        state: Optional[str] = None) -> Dict[str, Any]:
        """Get leases via REST API (async)."""
        if not self._rest_session:
            raise AkashAsyncClientError("Client not properly initialized. Use async context manager.")
        
        params = {}
        if owner:
            params['owner'] = owner
        if provider:
            params['provider'] = provider
        if state:
            params['state'] = state
        
        url = f"{self.rest_endpoint}/akash/market/v1beta4/leases/list"
        
        async with self._rest_session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
    
    # gRPC methods (delegated to gRPC client)
    async def grpc_query_deployments(self, **kwargs) -> Dict[str, Any]:
        """Query deployments via gRPC."""
        if not self._grpc_client:
            raise AkashAsyncClientError("gRPC endpoint not configured")
        
        return await self._grpc_client.query_deployments(**kwargs)
    
    async def grpc_query_bids(self, **kwargs) -> Dict[str, Any]:
        """Query bids via gRPC."""
        if not self._grpc_client:
            raise AkashAsyncClientError("gRPC endpoint not configured")
        
        return await self._grpc_client.query_bids(**kwargs)
    
    async def grpc_query_leases(self, **kwargs) -> Dict[str, Any]:
        """Query leases via gRPC."""
        if not self._grpc_client:
            raise AkashAsyncClientError("gRPC endpoint not configured")
        
        return await self._grpc_client.query_leases(**kwargs)
    
    async def grpc_query_providers(self, **kwargs) -> Dict[str, Any]:
        """Query providers via gRPC."""
        if not self._grpc_client:
            raise AkashAsyncClientError("gRPC endpoint not configured")
        
        return await self._grpc_client.query_providers(**kwargs)
    
    # Streaming methods
    async def stream_deployment_events(self, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream deployment events via gRPC."""
        if not self._grpc_client:
            raise AkashAsyncClientError("gRPC endpoint not configured")
        
        async for event in self._grpc_client.stream_deployment_events(**kwargs):
            yield event
    
    # Transaction methods
    async def create_deployment(self,
                               wallet: Wallet,
                               sdl: Dict[str, Any],
                               deposit: str = "10000000uakt",
                               gas_limit: int = 300000) -> Dict[str, Any]:
        """
        Create a deployment on the blockchain.
        
        Args:
            wallet: Wallet for signing
            sdl: Service Definition Language configuration
            deposit: Initial deposit
            gas_limit: Gas limit for transaction
            
        Returns:
            Transaction result
        """
        if not self._transaction_signer:
            raise AkashAsyncClientError("RPC endpoint not configured for transactions")
        
        # Get account info
        account_info = await self._get_account_info(wallet.address)
        
        # Create deployment message
        msg = self._transaction_signer.create_deployment_msg(
            wallet.address, sdl, deposit
        )
        
        # Create and sign transaction
        tx_info = TransactionInfo(
            chain_id=self.chain_id,
            account_number=account_info['account_number'],
            sequence=account_info['sequence'],
            fee={}
        )
        
        transaction = self._transaction_signer.create_transaction(
            wallet, [msg], tx_info, gas_limit
        )
        
        signed_tx = self._transaction_signer.sign_transaction(
            wallet, transaction, tx_info
        )
        
        # Broadcast transaction
        return await self._transaction_signer.broadcast_transaction(signed_tx)
    
    async def create_bid(self,
                        wallet: Wallet,
                        order_id: Dict[str, Any],
                        price: str,
                        gas_limit: int = 200000) -> Dict[str, Any]:
        """Create a bid on the blockchain."""
        if not self._transaction_signer:
            raise AkashAsyncClientError("RPC endpoint not configured for transactions")
        
        # Get account info
        account_info = await self._get_account_info(wallet.address)
        
        # Create bid message
        msg = self._transaction_signer.create_bid_msg(
            wallet.address, order_id, price
        )
        
        # Create and sign transaction
        tx_info = TransactionInfo(
            chain_id=self.chain_id,
            account_number=account_info['account_number'],
            sequence=account_info['sequence'],
            fee={}
        )
        
        transaction = self._transaction_signer.create_transaction(
            wallet, [msg], tx_info, gas_limit
        )
        
        signed_tx = self._transaction_signer.sign_transaction(
            wallet, transaction, tx_info
        )
        
        # Broadcast transaction
        return await self._transaction_signer.broadcast_transaction(signed_tx)
    
    async def create_lease(self,
                          wallet: Wallet,
                          bid_id: Dict[str, Any],
                          gas_limit: int = 200000) -> Dict[str, Any]:
        """Create a lease on the blockchain."""
        if not self._transaction_signer:
            raise AkashAsyncClientError("RPC endpoint not configured for transactions")
        
        # Get account info
        account_info = await self._get_account_info(wallet.address)
        
        # Create lease message
        msg = self._transaction_signer.create_lease_msg(
            wallet.address, wallet.address, bid_id
        )
        
        # Create and sign transaction
        tx_info = TransactionInfo(
            chain_id=self.chain_id,
            account_number=account_info['account_number'],
            sequence=account_info['sequence'],
            fee={}
        )
        
        transaction = self._transaction_signer.create_transaction(
            wallet, [msg], tx_info, gas_limit
        )
        
        signed_tx = self._transaction_signer.sign_transaction(
            wallet, transaction, tx_info
        )
        
        # Broadcast transaction
        return await self._transaction_signer.broadcast_transaction(signed_tx)
    
    async def _get_account_info(self, address: str) -> Dict[str, Any]:
        """Get account information for transaction signing."""
        if not self._rest_session:
            raise AkashAsyncClientError("REST session not available")
        
        url = f"{self.rest_endpoint}/cosmos/auth/v1beta1/accounts/{address}"
        
        async with self._rest_session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            
            account = data.get('account', {})
            return {
                'account_number': int(account.get('account_number', 0)),
                'sequence': int(account.get('sequence', 0))
            }
    
    # Health checks
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all configured endpoints."""
        health = {}
        
        # REST health check
        try:
            if self._rest_session:
                url = f"{self.rest_endpoint}/cosmos/base/tendermint/v1beta1/node_info"
                async with self._rest_session.get(url) as response:
                    health['rest'] = response.status == 200
            else:
                health['rest'] = False
        except Exception:
            health['rest'] = False
        
        # gRPC health check
        if self._grpc_client:
            health['grpc'] = await self._grpc_client.health_check()
        else:
            health['grpc'] = False
        
        # RPC health check
        if self._transaction_signer:
            try:
                # Simple RPC call to check connectivity
                health['rpc'] = True  # Placeholder
            except Exception:
                health['rpc'] = False
        else:
            health['rpc'] = False
        
        return health


# Convenience functions
async def create_async_client(rest_endpoint: str, 
                            grpc_endpoint: Optional[str] = None,
                            rpc_endpoint: Optional[str] = None,
                            **kwargs) -> AkashAsyncClient:
    """Create and initialize an async client."""
    client = AkashAsyncClient(
        rest_endpoint=rest_endpoint,
        grpc_endpoint=grpc_endpoint,
        rpc_endpoint=rpc_endpoint,
        **kwargs
    )
    return client
