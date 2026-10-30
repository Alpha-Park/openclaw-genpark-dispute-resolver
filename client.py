# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Dispute Resolver - Schelling Point Consensus & Dempster-Shafer Escrow Arbitrator
Standard Library only: math, typing.
Calculates decentralized Schelling-point consensus alignment, rewards consistent jurors while
slashing outliers, combines conflicting evidence via Dempster-Shafer theory, and determines
deterministic escrow settlement disbursement.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkDisputeResolver:
    def __init__(self, slashing_sensitivity: float = 1.5):
        self.sensitivity = slashing_sensitivity

    def calculate_schelling_consensus(self, juror_votes: List[Dict[str, Any]],
                                      stake_amount: float = 100.0) -> Dict[str, Any]:
        """
        Calculates Schelling point median consensus vote and adjusts juror reputation/stakes.
        Jurors voting close to the consensus median receive reward; outliers are slashed.
        """
        if not juror_votes:
            return {"consensus_value": 0.5, "jurors_evaluated": 0}

        # Extract votes (between 0.0 for buyer to 1.0 for seller)
        votes = [max(0.0, min(1.0, float(v.get("vote", 0.5)))) for v in juror_votes]
        weights = [max(0.1, float(v.get("stake", stake_amount))) for v in juror_votes]

        # Weighted median calculation
        total_weight = sum(weights)
        sorted_pairs = sorted(zip(votes, weights), key=lambda x: x[0])
        
        cumulative = 0.0
        median_vote = 0.5
        for v, w in sorted_pairs:
            cumulative += w
            if cumulative >= total_weight / 2.0:
                median_vote = v
                break

        # Compute consensus variance
        variance = sum(w * ((v - median_vote) ** 2) for v, w in zip(votes, weights)) / total_weight
        std_dev = math.sqrt(variance)

        juror_results = []
        slashed_pool = 0.0

        for j in juror_votes:
            v = max(0.0, min(1.0, float(j.get("vote", 0.5))))
            st = float(j.get("stake", stake_amount))
            distance = abs(v - median_vote)

            # Gaussian reward curve: exp(-dist^2 / (2 * sigma^2))
            sigma = max(0.1, std_dev)
            coherence = math.exp(- (distance ** 2) / (2.0 * (sigma ** 2)))

            if coherence >= 0.5:
                status = "REWARDED_CONSENSUS"
                payout = st * (1.0 + 0.10 * coherence)
            else:
                status = "SLASHED_OUTLIER"
                slash_fraction = min(0.50, (1.0 - coherence) * self.sensitivity * 0.25)
                slashed_amt = st * slash_fraction
                payout = st - slashed_amt
                slashed_pool += slashed_amt

            juror_results.append({
                "juror_id": j.get("juror_id", "juror_anon"),
                "vote": v,
                "distance_to_consensus": round(distance, 4),
                "coherence_score": round(coherence, 4),
                "disposition": status,
                "final_payout_usd": round(payout, 2)
            })

        return {
            "consensus_median_vote": round(median_vote, 4),
            "vote_dispersion_std_dev": round(std_dev, 4),
            "total_jurors": len(juror_votes),
            "total_slashed_stake_usd": round(slashed_pool, 2),
            "verdict": "RULE_IN_FAVOR_OF_SELLER" if median_vote > 0.65 else ("RULE_IN_FAVOR_OF_BUYER" if median_vote < 0.35 else "SPLIT_EQUITABLE_SETTLEMENT"),
            "juror_audit": juror_results
        }

    def combine_dempster_shafer_evidence(self, evidence_masses: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Combines multi-source belief masses for hypotheses: Buyer (B), Seller (S), Uncertainty (Theta).
        Each mass dict has keys: 'B', 'S', 'Theta' where sum = 1.0.
        Dempster's rule of combination:
        m12(A) = sum_{X cap Y = A} m1(X) m2(Y) / (1 - K)
        where K = sum_{X cap Y = empty} m1(X) m2(Y) is conflict.
        """
        if not evidence_masses:
            return {"belief_buyer": 0.5, "belief_seller": 0.5, "uncertainty": 0.0}

        current_m = evidence_masses[0]

        for m2 in evidence_masses[1:]:
            # Hypotheses combinations
            # B cap B = B; B cap Theta = B; Theta cap B = B
            # S cap S = S; S cap Theta = S; Theta cap S = S
            # Theta cap Theta = Theta
            # B cap S = empty (Conflict K)
            m1_B = current_m.get("B", 0.0)
            m1_S = current_m.get("S", 0.0)
            m1_T = current_m.get("Theta", 0.0)

            m2_B = m2.get("B", 0.0)
            m2_S = m2.get("S", 0.0)
            m2_T = m2.get("Theta", 0.0)

            # Conflict
            K = (m1_B * m2_S) + (m1_S * m2_B)
            denom = max(1e-6, 1.0 - K)

            comb_B = ((m1_B * m2_B) + (m1_B * m2_T) + (m1_T * m2_B)) / denom
            comb_S = ((m1_S * m2_S) + (m1_S * m2_T) + (m1_T * m2_S)) / denom
            comb_T = (m1_T * m2_T) / denom

            current_m = {"B": comb_B, "S": comb_S, "Theta": comb_T, "conflict_K": K}

        return {
            "combined_belief_buyer": round(current_m["B"], 4),
            "combined_belief_seller": round(current_m["S"], 4),
            "remaining_uncertainty": round(current_m["Theta"], 4),
            "conflict_metric_K": round(current_m.get("conflict_K", 0.0), 4)
        }

    def compute_escrow_settlement(self, buyer_claim: float, seller_claim: float,
                                 total_escrow_usd: float,
                                 buyer_support_prob: float) -> Dict[str, Any]:
        """
        Determines fair escrow split based on aggregate buyer support probability:
        Buyer share = total_escrow * buyer_support_prob
        Seller share = total_escrow * (1 - buyer_support_prob)
        """
        p_b = max(0.0, min(1.0, buyer_support_prob))
        buyer_payout = total_escrow_usd * p_b
        seller_payout = total_escrow_usd * (1.0 - p_b)

        return {
            "total_escrow_usd": total_escrow_usd,
            "buyer_claim_usd": buyer_claim,
            "seller_claim_usd": seller_claim,
            "buyer_support_probability": round(p_b, 4),
            "disbursed_to_buyer_usd": round(buyer_payout, 2),
            "disbursed_to_seller_usd": round(seller_payout, 2),
            "settlement_disposition": "FULL_REFUND_BUYER" if p_b > 0.85 else ("FULL_PAYOUT_SELLER" if p_b < 0.15 else "PROPORTIONAL_SPLIT")
        }
