from dataclasses import dataclass, field
import hashlib
import time
from typing import Optional

@dataclass
class Transaction:
    """
    Represents a Bitcoin transaction in the BIP 888 simulation.
    
    Attributes:
        sender (str): The sender's public address (bech32).
        receiver (str): The receiver's public address (bech32).
        amount (float): The amount of BTC transferred.
        is_real (bool): Flag indicating if this is a legitimate transaction.
        nonce (int): A unique nonce to differentiate identical transactions.
        timestamp (float): The time of creation.
        data (Optional[str]): Arbitrary payload data (used for decoy matching).
        tx_id (str): The calculated transaction ID (hash).
    """
    sender: str
    receiver: str
    amount: float
    is_real: bool = False
    nonce: int = 0
    timestamp: float = field(default_factory=time.time)
    data: Optional[str] = None
    tx_id: str = field(init=False)

    def __post_init__(self):
        """Calculates the transaction ID after initialization."""
        self.tx_id = self._calculate_id()

    def _calculate_id(self) -> str:
        """
        Generates a deterministic SHA-256 hash as the Transaction ID.
        
        Returns:
            str: The hexadecimal representation of the hash.
        """
        payload = f"{self.sender}{self.receiver}{self.amount}{self.nonce}{self.timestamp}{self.data}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "REAL" if self.is_real else "DECOY"
        return f"<Tx {self.tx_id[:8]}... | {status} | Amt={self.amount:.4f}>"
