"""
Transaction signing and blockchain interaction for Akash Network.

This module provides transaction creation, signing, and broadcasting capabilities
for the Akash blockchain.
"""

import json
import hashlib
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.backends import default_backend
    import ecdsa
    import bech32
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class AkashTransactionError(Exception):
    """Base exception for transaction-related errors."""
    pass


@dataclass
class TransactionInfo:
    """Transaction information structure."""
    chain_id: str
    account_number: int
    sequence: int
    fee: Dict[str, Any]
    memo: str = ""


@dataclass
class Wallet:
    """Wallet information for signing transactions."""
    private_key: bytes
    public_key: bytes
    address: str
    
    @classmethod
    def from_mnemonic(cls, mnemonic: str, derivation_path: str = "m/44'/118'/0'/0/0") -> 'Wallet':
        """Create wallet from mnemonic phrase."""
        if not CRYPTO_AVAILABLE:
            raise AkashTransactionError("Cryptography libraries required. Install with: pip install cryptography ecdsa bech32")
        
        # This would implement BIP39/BIP44 key derivation
        # For now, this is a placeholder
        raise NotImplementedError("Mnemonic wallet creation not yet implemented")
    
    @classmethod  
    def from_private_key(cls, private_key_hex: str) -> 'Wallet':
        """Create wallet from private key hex string."""
        if not CRYPTO_AVAILABLE:
            raise AkashTransactionError("Cryptography libraries required. Install with: pip install cryptography ecdsa bech32")
        
        try:
            # Convert hex to bytes
            private_key_bytes = bytes.fromhex(private_key_hex)
            
            # Create ECDSA private key
            signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
            verifying_key = signing_key.get_verifying_key()
            
            # Get public key bytes (compressed format)
            public_key_bytes = b'\x02' + verifying_key.to_string()[:32] if verifying_key.to_string()[63] % 2 == 0 else b'\x03' + verifying_key.to_string()[:32]
            
            # Generate address from public key
            pubkey_hash = hashlib.sha256(public_key_bytes).digest()
            ripemd160 = hashlib.new('ripemd160', pubkey_hash).digest()
            address = bech32.bech32_encode('akash', bech32.convertbits(ripemd160, 8, 5))
            
            return cls(
                private_key=private_key_bytes,
                public_key=public_key_bytes,
                address=address
            )
            
        except Exception as e:
            raise AkashTransactionError(f"Failed to create wallet from private key: {e}")


class AkashTransactionSigner:
    """
    Transaction signing and broadcasting for Akash Network.
    
    Handles transaction creation, signing with private keys, and broadcasting
    to the Akash blockchain.
    """
    
    def __init__(self, 
                 rpc_endpoint: str,
                 chain_id: str = "akashnet-2",
                 gas_price: str = "0.025uakt"):
        """
        Initialize transaction signer.
        
        Args:
            rpc_endpoint: Akash RPC endpoint
            chain_id: Blockchain chain ID
            gas_price: Default gas price
        """
        if not CRYPTO_AVAILABLE:
            raise AkashTransactionError("Cryptography libraries required for transaction signing")
        
        self.rpc_endpoint = rpc_endpoint.rstrip('/')
        self.chain_id = chain_id
        self.gas_price = gas_price
    
    def create_deployment_msg(self, 
                             owner: str,
                             sdl: Dict[str, Any],
                             deposit: str = "10000000uakt") -> Dict[str, Any]:
        """
        Create a deployment creation message.
        
        Args:
            owner: Deployment owner address
            sdl: Service Definition Language (SDL) configuration
            deposit: Initial deposit amount
            
        Returns:
            Message dictionary
        """
        return {
            "@type": "/akash.deployment.v1beta3.MsgCreateDeployment",
            "id": {
                "owner": owner,
                "dseq": "0"  # Will be set by the blockchain
            },
            "groups": self._sdl_to_groups(sdl),
            "version": base64.b64encode(json.dumps(sdl).encode()).decode(),
            "deposit": {
                "denom": "uakt",
                "amount": deposit.replace("uakt", "")
            },
            "depositor": owner
        }
    
    def create_bid_msg(self,
                      bidder: str,
                      order_id: Dict[str, Any],
                      price: str) -> Dict[str, Any]:
        """
        Create a bid creation message.
        
        Args:
            bidder: Bidder address
            order_id: Order identifier
            price: Bid price
            
        Returns:
            Message dictionary
        """
        return {
            "@type": "/akash.market.v1beta4.MsgCreateBid",
            "order": order_id,
            "provider": bidder,
            "price": {
                "denom": "uakt",
                "amount": price.replace("uakt", "")
            }
        }
    
    def create_lease_msg(self,
                        tenant: str,
                        provider: str,
                        bid_id: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a lease creation message.
        
        Args:
            tenant: Tenant address
            provider: Provider address  
            bid_id: Bid identifier
            
        Returns:
            Message dictionary
        """
        return {
            "@type": "/akash.market.v1beta4.MsgCreateLease",
            "bid_id": bid_id
        }
    
    def create_transaction(self,
                          wallet: Wallet,
                          messages: List[Dict[str, Any]],
                          tx_info: TransactionInfo,
                          gas_limit: int = 200000) -> Dict[str, Any]:
        """
        Create a complete transaction ready for signing.
        
        Args:
            wallet: Wallet for signing
            messages: List of transaction messages
            tx_info: Transaction metadata
            gas_limit: Gas limit for transaction
            
        Returns:
            Transaction dictionary
        """
        # Calculate fee
        gas_amount = int(float(self.gas_price.replace("uakt", "")) * gas_limit)
        
        return {
            "body": {
                "messages": messages,
                "memo": tx_info.memo,
                "timeout_height": "0",
                "extension_options": [],
                "non_critical_extension_options": []
            },
            "auth_info": {
                "signer_infos": [{
                    "public_key": {
                        "@type": "/cosmos.crypto.secp256k1.PubKey",
                        "key": base64.b64encode(wallet.public_key).decode()
                    },
                    "mode_info": {
                        "single": {
                            "mode": "SIGN_MODE_DIRECT"
                        }
                    },
                    "sequence": str(tx_info.sequence)
                }],
                "fee": {
                    "amount": [{
                        "denom": "uakt",
                        "amount": str(gas_amount)
                    }],
                    "gas_limit": str(gas_limit),
                    "payer": "",
                    "granter": ""
                }
            },
            "signatures": []
        }
    
    def sign_transaction(self,
                        wallet: Wallet,
                        transaction: Dict[str, Any],
                        tx_info: TransactionInfo) -> Dict[str, Any]:
        """
        Sign a transaction with the wallet's private key.
        
        Args:
            wallet: Wallet for signing
            transaction: Transaction to sign
            tx_info: Transaction metadata
            
        Returns:
            Signed transaction
        """
        # Create signing document
        sign_doc = {
            "body_bytes": self._encode_body(transaction["body"]),
            "auth_info_bytes": self._encode_auth_info(transaction["auth_info"]),
            "chain_id": tx_info.chain_id,
            "account_number": str(tx_info.account_number)
        }
        
        # Create signature
        sign_bytes = json.dumps(sign_doc, sort_keys=True, separators=(',', ':')).encode()
        signature_hash = hashlib.sha256(sign_bytes).digest()
        
        # Sign with ECDSA
        signing_key = ecdsa.SigningKey.from_string(wallet.private_key, curve=ecdsa.SECP256k1)
        signature = signing_key.sign(signature_hash, hashfunc=hashlib.sha256)
        
        # Add signature to transaction
        transaction["signatures"] = [base64.b64encode(signature).decode()]
        
        return transaction
    
    async def broadcast_transaction(self, signed_tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast a signed transaction to the blockchain.
        
        Args:
            signed_tx: Signed transaction
            
        Returns:
            Broadcast response
        """
        import aiohttp
        
        broadcast_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "broadcast_tx_commit",
            "params": {
                "tx": base64.b64encode(json.dumps(signed_tx).encode()).decode()
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.rpc_endpoint}/", json=broadcast_data) as response:
                result = await response.json()
                
                if "error" in result:
                    raise AkashTransactionError(f"Broadcast failed: {result['error']}")
                
                return result["result"]
    
    def _sdl_to_groups(self, sdl: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert SDL to deployment groups."""
        # This would parse SDL and create proper group specifications
        # Placeholder implementation
        return [{
            "name": "default",
            "requirements": {
                "signed_by": {
                    "all_of": [],
                    "any_of": []
                }
            },
            "resources": [{
                "resources": {
                    "cpu": {
                        "units": {
                            "val": "1000"
                        }
                    },
                    "memory": {
                        "quantity": {
                            "val": "1073741824"
                        }
                    },
                    "storage": [{
                        "name": "default",
                        "quantity": {
                            "val": "1073741824"
                        }
                    }]
                },
                "count": 1,
                "price": {
                    "denom": "uakt",
                    "amount": "1000"
                }
            }]
        }]
    
    def _encode_body(self, body: Dict[str, Any]) -> bytes:
        """Encode transaction body for signing."""
        # This would use proper protobuf encoding
        return json.dumps(body, sort_keys=True).encode()
    
    def _encode_auth_info(self, auth_info: Dict[str, Any]) -> bytes:
        """Encode auth info for signing."""
        # This would use proper protobuf encoding
        return json.dumps(auth_info, sort_keys=True).encode()


# Convenience functions
def create_wallet_from_private_key(private_key_hex: str) -> Wallet:
    """Create a wallet from a private key hex string."""
    return Wallet.from_private_key(private_key_hex)


def create_signer(rpc_endpoint: str, chain_id: str = "akashnet-2") -> AkashTransactionSigner:
    """Create a transaction signer instance."""
    return AkashTransactionSigner(rpc_endpoint, chain_id)
