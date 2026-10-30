# -*- coding: utf-8 -*-
from client import OpenClawGenParkDisputeResolver

resolver = OpenClawGenParkDisputeResolver()

# 1. Schelling Consensus
votes = [
    {"juror_id": "j1", "vote": 0.20, "stake": 100.0},
    {"juror_id": "j2", "vote": 0.25, "stake": 100.0},
    {"juror_id": "j3", "vote": 0.15, "stake": 150.0},
    {"juror_id": "j4", "vote": 0.90, "stake": 100.0} # outlier
]
cons = resolver.calculate_schelling_consensus(votes)
print(f"Schelling Consensus Median: {cons['consensus_median_vote']} -> {cons['verdict']}")
print(f"  Slashed Stake: ${cons['total_slashed_stake_usd']}")

# 2. Dempster-Shafer Evidence Combination
evidence = [
    {"B": 0.70, "S": 0.10, "Theta": 0.20}, # Telemetry sensor log
    {"B": 0.60, "S": 0.20, "Theta": 0.20}  # Cryptographic receipt audit
]
comb = resolver.combine_dempster_shafer_evidence(evidence)
print(f"\nCombined Belief: Buyer={comb['combined_belief_buyer']}, Seller={comb['combined_belief_seller']}")

# 3. Escrow Settlement
settlement = resolver.compute_escrow_settlement(buyer_claim=500.0, seller_claim=500.0, total_escrow_usd=500.0, buyer_support_prob=comb['combined_belief_buyer'])
print(f"\nSettlement: Buyer=${settlement['disbursed_to_buyer_usd']}, Seller=${settlement['disbursed_to_seller_usd']} ({settlement['settlement_disposition']})")
