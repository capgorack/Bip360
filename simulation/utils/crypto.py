"""
Cryptographic utility functions for the BIP 888 simulation.
Includes chaotic map generators and hashing helpers.
"""

import hashlib
import struct
from typing import Generator

def logistic_map(x: float, r: float = 3.9999) -> float:
    """
    Computes the next value in the logistic map sequence.
    Formula: x_{n+1} = r * x_n * (1 - x_n)
    
    Args:
        x (float): Current value (must be between 0 and 1).
        r (float): Growth rate parameter (default 3.9999 for chaotic behavior).
        
    Returns:
        float: The next value in the sequence (normalized).
    """
    return r * x * (1 - x)

def generate_chaotic_seed(data: str) -> float:
    """
    Generates a deterministic float seed from input data using SHA-256.
    
    Args:
        data (str): Input string to hash.
        
    Returns:
        float: A value between 0.0 and 1.0 derived from the hash.
    """
    hash_bytes = hashlib.sha256(data.encode()).digest()
    # Interpret the first 8 bytes as an unsigned long long (big-endian)
    seed_int = struct.unpack(">Q", hash_bytes[:8])[0]
    # Normalize to [0, 1]
    return (seed_int % 1_000_000) / 1_000_000.0

def chaotic_sequence(start_val: float, length: int, warmup: int = 100) -> Generator[float, None, None]:
    """
    Yields a sequence of chaotic values from a starting seed.
    
    Args:
        start_val (float): Initial seed value.
        length (int): Number of values to generate.
        warmup (int): Number of iterations to discard (to remove transient behavior).
        
    Yields:
        float: Next chaotic value.
    """
    x = start_val
    # Warmup phase
    for _ in range(warmup):
        x = logistic_map(x)
        
    # Generation phase
    for _ in range(length):
        x = logistic_map(x)
        yield x
