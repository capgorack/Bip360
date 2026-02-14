"""
Quantum Adversary Simulation Module for BIP 888.
Simulates an attacker attempting to break ECC using Grover's Algorithm on a Transaction Swarm.
"""

import math
from typing import List, Dict, Union

from simulation.models.transaction import Transaction

class QuantumAdversary:
    """
    Represents a quantum computer attempting to find the private key of a transaction.
    Uses Grover's algorithm to search the decoy space.
    """

    def __init__(self, qubits: int = 1000, coherence_time_ms: int = 1000):
        """
        Args:
            qubits (int): Number of coherent qubits available to the attacker.
            coherence_time_ms (int): Time in milliseconds the qubits can maintain state.
        """
        self.qubits = qubits
        self.coherence_time_ms = coherence_time_ms
        # Simplified metric: Computational operations per millisecond
        # Assuming linear scaling for now, though real scaling is more complex
        self.ops_per_ms = qubits * 1000 

    def estimate_grover_iterations(self, search_space_size: int) -> float:
        """
        Calculates the optimal number of iterations for Grover's algorithm.
        O(sqrt(N)) complexity.
        
        Args:
            search_space_size (int): Total number of items to search (N).
            
        Returns:
            float: Approximate number of iterations required (~ (pi/4) * sqrt(N)).
        """
        if search_space_size <= 0:
            return 0.0
        return (math.pi / 4) * math.sqrt(search_space_size)

    def attack(self, swarm: List[Transaction], block_time_sec: int = 600) -> Dict[str, Union[bool, float, int]]:
        """
        Simulates an attack on the transaction swarm within a block interval.
        
        Args:
            swarm (List[Transaction]): The list of transactions (1 real + N decoys).
            block_time_sec (int): The target time window (e.g., 10 minutes for Bitcoin).
            
        Returns:
            Dict: Simulation results including success status and time taken.
        """
        n_items = len(swarm)
        required_iterations = self.estimate_grover_iterations(n_items)
        
        # Computational Cost Model:
        # Each check (oracle call) involves verifying a signature or hash.
        # Let's assume a cost 'C' operations per check.
        c_ops_per_check = 2000  # Adjusted cost slightly higher for realism
        
        total_ops_needed = required_iterations * c_ops_per_check
        
        # Calculate Attack Speed
        # ops_per_ms * 1000 = ops per second
        ops_per_sec = self.ops_per_ms * 1000
        
        if ops_per_sec == 0:
            time_needed_sec = float('inf')
        else:
            time_needed_sec = total_ops_needed / ops_per_sec
        
        # Quantum Error Correction Overhead
        # Real QC require significant overhead. We add a factor.
        overhead_factor = 1.5
        time_needed_sec *= overhead_factor
        
        success = time_needed_sec < block_time_sec
        
        return {
            "success": success,
            "time_needed": time_needed_sec,
            "required_iterations": int(required_iterations),
            "swarm_size": n_items,
            "attacker_qubits": self.qubits
        }
