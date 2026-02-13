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

# Reference Implementation
*(To be added)*
Phase 1 simulation logic is currently being developed to demonstrate the entropy threshold required to defeat a simulated growing quantum adversary.

# Security Considerations
- **Bandwidth:** The primary cost is network bandwidth. This can be mitigated by "Compact Decoys" where only the seed to generate the decoy is transmitted, and nodes regenerate the full decoy locally.
- **DoS:** Care must be taken to ensure the decoy generation generation itself cannot be used as a vector for Denial of Service against validators.

