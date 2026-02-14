<preamble>
  BIP: [TBD]
  Layer: Consensus (Soft Fork)
  Title: Entropic Swarm Shield (ESS) - Quantum Resistance via Distributed Decoys
  Author: CapGorack <contact@bip360.org>
  Status: Draft
  Type: Standards Track
  Created: 2026-02-13
  License: BSD-2-Clause
</preamble>

# Abstract
This BIP proposes a novel defense mechanism against quantum computing attacks (specifically, Grover's algorithm targeting ECDSA private keys from public keys revealed in the mempool). The proposed solution, the **Entropic Swarm Shield (ESS)**, utilizes the distributed computational power of the validator network to generate massive volumes of cryptographically plausible decoy transactions for every legitimate transaction. This "Fractal Mimicry Protocol" creates an informational asymmetry: while the legitimate network can cheaply verify validity via a time-locked shared secret, a quantum adversary is forced to expend exponential resources distinguishing the target from the noise, effectively neutralizing the quantum advantage through brute-force entropy.

# Copyright
This document is licensed under the 2-clause BSD license.

# Motivation
The vulnerability of Elliptic Curve Cryptography (ECC) to Shor's algorithm is a known existential threat to Bitcoin. While Post-Quantum Cryptography (PQC) signatures (e.g., Lamport, lattice-based) offer a solution, they often come with significant block space overhead. Furthermore, the "harvest now, decrypt later" threat model does not apply to active transaction signing, but the "sniper" attack—deriving a private key from the public key revealed in a broadcast transaction before it is mined—remains critical.
The current defense is passive (mathematical hardness). We propose an active defense: **obfuscation through distributed work**. By leveraging the idle computational capacity of the network to generate noise, we can increase the effective bit-security of the mempool against real-time quantum attacks without requiring immediate, fundamental changes to the underlying signature scheme.

# Specification

## 1. Fractal Decoy Generation
Upon receiving a transaction $T_{real}$, participating nodes MUST generate $N$ decoy transactions $T_{decoy}$.
- **Determinism:** Decoys are generated using a deterministic chaotic map (e.g., Logistic Map or Mandelbrot set coordinates) seeded by $T_{real}$'s hash and a rolling network nonce.
- **Indistinguishability:** Decoys MUST share the exact data structure, byte size, and fee market characteristics of $T_{real}$.
- **Ratio:** The network targets a dynamic decoy-to-real ratio $R$, adjustable based on perceived threat levels (e.g., $R=10,000$).

## 2. Consenso Seletivo (Selective Consensus) via Time-Lock
To prevent the network from processing invalid decoys, a validity axiom is introduced:
- A transaction is valid only if it satisfies a lightweight Proof-of-Work (PoW) or Proof-of-Stake (PoS) condition that is computationally inexpensive for a verifier but impossible for an attacker to pre-calculate for all decoys simultaneously.
- **Mechanism:** $Hash(T_{real} + BlockHeight_{prev}) \mod Difficulty \equiv Secret_{shared}$.
- This shared secret is derived from a ephemeral key exchange or a verifiable delay function (VDF) that resolves only when the block is found.

## 3. Storage and Pruning
Decoys exist ONLY in the mempool and p2p propagation layer.
- Validators include only $T_{real}$ in the block candidate.
- Upon block propagation, all nodes discard $T_{decoy}$ associated with the confirmed $T_{real}$.
- This ensures zero bloat to the permanent blockchain (Time-Space Trade-off).

# Rationale
## Why Active Defense?
Passive upgrades to PQC require a hard fork and massive block size increases. ESS acts as a "soft shield" that can be deployed as a layer-0 network upgrade or a soft fork, protecting legacy addresses without requiring user action.

## Why Fractal Generation?
Random noise is easily filterable. Fractal noise maintains statistical properties similar to real data (Zipf's law, Benford's law), forcing the attacker to fully process each candidate.

# Backwards Compatibility
This proposal requires a Soft Fork.
- Behaving nodes: Will see a flood of transactions but only confirm valid ones based on the new consensus rule.
- Legacy nodes: May initially reject the high volume of traffic or see it as spam. A new P2P message type `INV_DECOY` may be required to segregate traffic and prevent legacy node banlisting.

# Threat Modeling
To evaluate the effectiveness of ESS, we compare the following security scenarios:

1.  **Baseline (No Defense)**: Transactions reveal public keys in the mempool. A CRQC derivations of the private key within $T < 600s$ results in a successful theft via conflicting transaction (RBF or high-fee double spend).
2.  **ESS Shield (BIP 888)**: The mempool is populated with $N=10^5$ decoys. The adversary must execute Grover searches across the swarm. The resulting search time $T_{search} \gg 600s$ ensures the transaction is confirmed before the key is derived.
3.  **Full PQC (Future State)**: Cryptographic primitives are replaced with lattice/hash-based signatures. While providing absolute mathematical resistance, this requires significant block space and a major consensus overhaul. ESS serves as the "Pre-Quantum" bridge.

# Open Questions & Considerations
- **Scalability**: A decoy swarm of $10^5$ generates significant overhead. We propose "Compressed Decoys" (sending seeds rather than full data) to quantify and minimize MB/s impact per node.
- **Relay Policies**: Bitcoin nodes use strict anti-spam and fee filters. Decoys must be "economically plausible" to avoid being pruned by relay policy before serving their defensive purpose.
- **Adaptive Attacks**: An adversary may attempt to distinguish decoys using heuristics (creation timing, fee patterns). ESS must ensure the "plausibility" of decoys through statistical alignment with real-world mempool behavior.
- **Grover implementation**: The cost of the SHA-256 Oracle in a CRQC environment needs further formalization to establish precise security margins across optimistic/pessimistic hardware scenarios.

# Reference Implementation
*(To be added)*
Phase 1 simulation logic is currently being developed to demonstrate the entropy threshold required to defeat a simulated growing quantum adversary.

# 6. Advanced Mechanics & Governance

## 6.1 Decoy Indistinguishability (Active Camouflage)
To prevent heuristic filtering, the chaotic map generators are parameterized by real-time mempool statistics:
- **Fee Mimicry**: Decoy fees are drawn from a distribution $D_{fee}$ matching the rolling average of the last $k$ blocks.
- **Script Templating**: Decoy script types (P2TR, P2WPKH) mirror the ratios observed in the current mempool.
- **Result**: An adversary cannot simply filter by "low fee" or "non-standard script" without rejecting a significant portion of legitimate traffic.

## 6.2 Relay Policy & Anti-Spam (Receiver-PoW)
To prevent network flooding, ESS introduces a **Receiver-Proof-of-Work** mechanism:
- **Compact Propagation**: Nodes propagate `INV_ENTROPY` messages containing only the Seed (32 bytes).
- **Local Inflation**: The receiving node performs the chaotic expansion locally.
- **Cost Asymmetry**: Validating the seed's PoW is cheap; generating the full swarm is computationally strictly bounded. This shifts the bandwidth cost from the network P2P layer to local CPU/Memory, which is abundant compared to block space.

## 6.3 Seed Security
The seed $S$ is ephemeral and derived from:
$$S = Hash(Block_{prev} \oplus Node_{nonce} \oplus TimeSlot)$$
- **Local Scope**: The seed is valid only for the current propagation window.
- **Unpredictability**: An attacker cannot pre-calculate the swarm without compromising the underlying PoW entropy of the previous block or the specific node's state.

## 6.4 Governance & Activation
- **Soft Fork Required**: ESS introduces a new consensus rule for `INV_ENTROPY` propagation and Time-Lock validation.
- **Backward Compatibility**: Legacy nodes will simply ignore `INV_ENTROPY` messages. The swarm protection will effectively form an overlay network of upgraded nodes that shield the transaction until it reaches a miner (who may or may not be upgraded, but the delay is achieved during propagation).

# Security Considerations
- **Bandwidth:** The primary cost is network bandwidth. This can be mitigated by "Compact Decoys" where only the seed to generate the decoy is transmitted, and nodes regenerate the full decoy locally.
- **DoS:** Care must be taken to ensure the decoy generation itself cannot be used as a vector for Denial of Service against validators.
