"""
Simulation Runner for BIP 888.
Orchestrates the interplay between the Entropic Swarm and the Quantum Adversary.
"""

import sys
import os
import argparse
import time

# Ensure the simulation package is importable
# Add the project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from simulation.core.swarm import SwarmGenerator
from simulation.core.consensus import Validator
from simulation.adversary.quantum import QuantumAdversary

def run_simulation(decoys: int, qubits: int, block_time: int) -> dict:
    """
    Runs a single simulation iteration.
    
    Args:
        decoys (int): Number of decoy transactions.
        qubits (int): Number of qubits available to the attacker.
        block_time (int): Block time in seconds.
        
    Returns:
        dict: Results of the simulation run.
    """
    print(f"\n[Scenario] Swarm Size: {decoys} | Qubits: {qubits} | Block Time: {block_time}s")
    
    # Initialize agents
    swarm_gen = SwarmGenerator(decoy_ratio=decoys)
    adversary = QuantumAdversary(qubits=qubits)
    validator = Validator(shared_secret_difficulty=10000)
    
    # 1. Generate Swarm
    start_gen = time.time()
    swarm = swarm_gen.create_swarm("sender_addr", "receiver_addr", 1.0)
    gen_time = time.time() - start_gen
    print(f"  -> Generated {len(swarm)} transactions in {gen_time:.4f}s")
    
    # 2. Simulate Attack
    result = adversary.attack(swarm, block_time_sec=block_time)
    
    # 3. Simulate Consensus Validation (sanity check)
    real_tx = next((tx for tx in swarm if tx.is_real), None)
    is_valid = validator.verify_time_lock(real_tx, "seed") if real_tx else False
    
    status_icon = "❌ CRACKED" if result['success'] else "✅ SECURE"
    margin = result['time_needed'] - block_time
    
    print(f"  -> {status_icon}")
    print(f"     Time to Crack: {result['time_needed']:.4f}s")
    if result['success']:
        print(f"     Attacker WON by {-margin:.2f}s")
    else:
        print(f"     Network HELD by {margin:.2f}s")
        
    return result

def main():
    parser = argparse.ArgumentParser(description="BIP 888 Entropic Swarm Shield Simulation")
    parser.add_argument("--decoys", type=int, default=1000, help="Number of decoy transactions per real tx")
    parser.add_argument("--qubits", type=int, default=1000, help="Number of qubits available to the attacker")
    parser.add_argument("--block-time", type=int, default=600, help="Block time in seconds (default: 600)")
    parser.add_argument("--run-all", action="store_true", help="Run a predefined suite of scenarios")
    
    args = parser.parse_args()
    
    print("==================================================")
    print("   BIP 888: ENTROPIC SWARM SHIELD SIMULATION")
    print("==================================================")
    
    if args.run_all:
        scenarios = [
            {"decoys": 10, "qubits": 100},
            {"decoys": 1000, "qubits": 100},
            {"decoys": 1000, "qubits": 5000},
            {"decoys": 100000, "qubits": 5000},
            {"decoys": 1000000, "qubits": 10000},
        ]
        
        for scen in scenarios:
            run_simulation(decoys=scen['decoys'], qubits=scen['qubits'], block_time=args.block_time)
    else:
        run_simulation(decoys=args.decoys, qubits=args.qubits, block_time=args.block_time)
        
    print("\nSimulation Complete.")

if __name__ == "__main__":
    main()
