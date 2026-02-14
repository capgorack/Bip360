"""
Swarm Generation Module for BIP 888.
Orchestrates the creation of legitimate transactions and their associated fractal decoys.
"""

import hashlib
import random
from typing import List, Generator

from simulation.models.transaction import Transaction
from simulation.utils.crypto import generate_chaotic_seed, chaotic_sequence

class SwarmGenerator:
    """
    Generates a swarm of transactions consisting of one real transaction and N decoys.
    Uses chaotic maps to ensure deterministic yet pseudo-random properties for decoys.
    """

    def __init__(self, decoy_ratio: int = 1000):
        """
        Args:
            decoy_ratio (int):Number of decoy transactions to generate per real transaction.
        """
        self.decoy_ratio = decoy_ratio

    def create_swarm(self, sender: str, receiver: str, amount: float) -> List[Transaction]:
        """
        Creates a list of transactions containing one real transaction and N decoys.
        
        Args:
            sender (str): The sender's address.
            receiver (str): The receiver's address.
            amount (float): The amount to transfer.
            
        Returns:
            List[Transaction]: A shuffled list of transactions.
        """
        # 1. Create the legitimate transaction
        real_tx = Transaction(sender=sender, receiver=receiver, amount=amount, is_real=True)
        
        swarm = [real_tx]
        
        # 2. Generate Decoys using Chaotic Map
        # Seed derived from the real transaction's ID and timestamp for determinism per tx
        seed_data = f"{real_tx.tx_id}{real_tx.timestamp}"
        initial_seed = generate_chaotic_seed(seed_data)
        
        # Generator for chaotic values
        chaos_gen = chaotic_sequence(start_val=initial_seed, length=self.decoy_ratio)
        
        for i, chaotic_val in enumerate(chaos_gen):
            # Generate deterministic decoy attributes based on chaotic state
            # Decoy amount varies slightly around the real amount (+/- 10%)
            variation = (chaotic_val * 0.2) - 0.1  # Range [-0.1, 0.1]
            fake_amount = amount * (1.0 + variation)
            
            # Decoy receiver address is a hash derived from the real receiver and index
            fake_receiver = hashlib.sha256(f"{receiver}{i}".encode()).hexdigest()[:34]
            
            # Create decoy transaction
            # Nonce ensures uniqueness even if other attributes collide
            decoy = Transaction(
                sender=sender,
                receiver=fake_receiver,
                amount=fake_amount, 
                is_real=False, 
                nonce=i
            )
            swarm.append(decoy)
            
        # 3. Shuffle (Simulate Network Propagation Mixing)
        # In a real network, transactions arrive asynchronously. Here we shuffle.
        random.shuffle(swarm)
        
        return swarm
