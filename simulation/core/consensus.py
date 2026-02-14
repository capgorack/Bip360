"""
Consensus Logic Module for BIP 888.
Handles the validation of transactions using the Time-Locked Puzzle mechanism.
"""

from typing import Optional
from simulation.models.transaction import Transaction

class Validator:
    """
    Simulates a network validator node.
    Responsible for identifying the single valid transaction within a swarm using a shared secret.
    """

    def __init__(self, shared_secret_difficulty: int = 1000):
        """
        Args:
            shared_secret_difficulty (int): Difficulty parameter for the time-lock puzzle simulation.
        """
        self.difficulty = shared_secret_difficulty

    def verify_time_lock(self, tx: Transaction, block_seed: str) -> bool:
        """
        Simulates the verification of a transaction against a time-lock puzzle.
        In a real scenario, this would involve solving a VDF or checking a PoW condition against the block seed.
        
        For simulation simplicity, we check the `is_real` flag (which represents possessing the correct solution).
        In a full implementation, this would be:
        Hash(Tx + BlockSeed) % Difficulty == Secret
        
        Args:
            tx (Transaction): The transaction to verify.
            block_seed (str): The seed for the current block (time-lock key).
            
        Returns:
            bool: True if the transaction satisfies the time-lock condition, False otherwise.
        """
        # Simulation abstraction: Only the real transaction successfully validates
        # In reality, this check is computationally cheap for the validator 
        # but expensive for an attacker to spoof for N decoys simultaneously.
        if tx.is_real:
            return True
            
        # Decoys fail the specific mathematical condition
        return False

    def find_valid_transaction(self, swarm: list[Transaction], block_seed: str) -> Optional[Transaction]:
        """
        Scans a swarm of transactions to find the valid one.
        
        Args:
            swarm (list[Transaction]): List of candidate transactions.
            block_seed (str): The current block's time-lock seed.
            
        Returns:
            Optional[Transaction]: The valid transaction if found, else None.
        """
        for tx in swarm:
            if self.verify_time_lock(tx, block_seed):
                return tx
        return None
