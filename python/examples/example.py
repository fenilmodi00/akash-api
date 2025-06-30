#!/usr/bin/env python3
"""
Example usage of the Akash Network Python SDK.

This demonstrates basic operations using the Python SDK for the Akash Network API.
"""

from akash_api import AkashClient, AkashClientError

def main():
    """Example usage of the Akash Python SDK."""
    
    # Initialize the client with an Akash REST endpoint
    client = AkashClient("https://api.akash.network")
    
    try:
        # Query deployments
        print("Fetching deployments...")
        deployments = client.get_deployments()
        print(f"Found {len(deployments.get('deployments', []))} deployments")
        
        # Query providers
        print("\nFetching providers...")
        providers = client.get_providers()
        print(f"Found {len(providers.get('providers', []))} providers")
        
        # Query market activity
        print("\nFetching market activity...")
        bids = client.get_bids()
        leases = client.get_leases()
        print(f"Found {len(bids.get('bids', []))} bids")
        print(f"Found {len(leases.get('leases', []))} leases")
        
        print("\n✓ All operations completed successfully!")
        
    except AkashClientError as e:
        print(f"Akash API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
