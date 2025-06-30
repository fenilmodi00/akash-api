"""
High-level client for interacting with the Akash Network API.

This client provides a simplified interface for common operations.
"""

import logging
from typing import Optional, Dict, Any, List

# Try to import requests, fallback to a simple mock if not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    # Simple mock for when requests is not available
    class MockResponse:
        def json(self):
            return {"message": "requests module not available - install with: pip install requests"}
        def raise_for_status(self):
            pass
    
    class requests:
        class exceptions:
            RequestException = Exception
        
        @staticmethod
        def get(url, params=None, timeout=None):
            return MockResponse()


class AkashClientError(Exception):
    """Base exception for Akash client errors."""
    pass


class AkashClient:
    """
    High-level client for interacting with the Akash Network.
    
    This client provides methods for common operations like querying deployments,
    bids, leases, and providers. It works with REST endpoints.
    """
    
    def __init__(self, 
                 rest_endpoint: str,
                 timeout: int = 30):
        """
        Initialize the Akash client.
        
        Args:
            rest_endpoint: The REST API endpoint URL (e.g., "https://api.akash.network")
            timeout: Request timeout in seconds
        """
        self.rest_endpoint = rest_endpoint.rstrip('/')
        self.timeout = timeout
    
    def _make_rest_request(self, path: str, params: Optional[Dict] = None) -> Dict[Any, Any]:
        """Make a REST API request."""
        url = f"{self.rest_endpoint}/{path.lstrip('/')}"
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise AkashClientError(f"REST request failed: {e}")
    
    # Deployment methods
    def get_deployments(self, 
                       owner: Optional[str] = None, 
                       state: Optional[str] = None,
                       dseq: Optional[int] = None) -> Dict[Any, Any]:
        """
        Get deployments based on filter criteria.
        
        Args:
            owner: Filter by deployment owner address
            state: Filter by deployment state (active, closed)
            dseq: Filter by deployment sequence number
            
        Returns:
            Dictionary containing deployment data
        """
        params = {}
        if owner:
            params['owner'] = owner
        if state:
            params['state'] = state
        if dseq:
            params['dseq'] = str(dseq)
        
        return self._make_rest_request('/akash/deployment/v1beta3/deployments', params)
    
    def get_deployment(self, owner: str, dseq: int) -> Dict[Any, Any]:
        """
        Get a specific deployment by owner and sequence number.
        
        Args:
            owner: The deployment owner address
            dseq: The deployment sequence number
            
        Returns:
            Dictionary containing deployment data
        """
        path = f'/akash/deployment/v1beta3/deployments/{owner}/{dseq}'
        return self._make_rest_request(path)
    
    # Market methods
    def get_bids(self, 
                 owner: Optional[str] = None,
                 dseq: Optional[int] = None,
                 gseq: Optional[int] = None,
                 oseq: Optional[int] = None,
                 provider: Optional[str] = None,
                 state: Optional[str] = None) -> Dict[Any, Any]:
        """
        Get bids based on filter criteria.
        
        Args:
            owner: Filter by deployment owner
            dseq: Filter by deployment sequence
            gseq: Filter by group sequence  
            oseq: Filter by order sequence
            provider: Filter by provider address
            state: Filter by bid state
            
        Returns:
            Dictionary containing bid data
        """
        params = {}
        for key, value in [
            ('owner', owner), ('dseq', dseq), ('gseq', gseq), 
            ('oseq', oseq), ('provider', provider), ('state', state)
        ]:
            if value is not None:
                params[key] = str(value)
        
        return self._make_rest_request('/akash/market/v1beta4/bids/list', params)
    
    def get_leases(self,
                   owner: Optional[str] = None,
                   dseq: Optional[int] = None,
                   gseq: Optional[int] = None,
                   oseq: Optional[int] = None,
                   provider: Optional[str] = None,
                   state: Optional[str] = None) -> Dict[Any, Any]:
        """
        Get leases based on filter criteria.
        
        Args:
            owner: Filter by deployment owner
            dseq: Filter by deployment sequence
            gseq: Filter by group sequence
            oseq: Filter by order sequence  
            provider: Filter by provider address
            state: Filter by lease state
            
        Returns:
            Dictionary containing lease data
        """
        params = {}
        for key, value in [
            ('owner', owner), ('dseq', dseq), ('gseq', gseq),
            ('oseq', oseq), ('provider', provider), ('state', state)
        ]:
            if value is not None:
                params[key] = str(value)
        
        return self._make_rest_request('/akash/market/v1beta4/leases/list', params)
    
    # Provider methods
    def get_providers(self) -> Dict[Any, Any]:
        """
        Get list of active providers.
        
        Returns:
            Dictionary containing provider data
        """
        return self._make_rest_request('/akash/provider/v1beta3/providers')
    
    def get_provider(self, address: str) -> Dict[Any, Any]:
        """
        Get information about a specific provider.
        
        Args:
            address: The provider address
            
        Returns:
            Dictionary containing provider data
        """
        path = f'/akash/provider/v1beta3/providers/{address}'
        return self._make_rest_request(path)
    
    # Utility methods
    def health_check(self) -> bool:
        """
        Check if the configured endpoint is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Try a simple query that should always work
            self._make_rest_request('/akash/deployment/v1beta3/deployments', {'limit': '1'})
            return True
        except Exception:
            return False
