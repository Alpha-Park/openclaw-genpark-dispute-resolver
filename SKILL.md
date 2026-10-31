---
name: openclaw-genpark-dispute-resolver
description: OpenClaw GenPark Dispute Resolver - Schelling point consensus and Dempster-Shafer escrow arbitrator with stake slashing and proportional settlement.
category: Service
version: 1.0.0
license: MIT
tools:
  - calculate_schelling_consensus
  - combine_dempster_shafer_evidence
  - compute_escrow_settlement
---

# Openclaw Genpark Dispute Resolver

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Openclaw Genpark Dispute Resolver**.
Your primary directive is to execute: OpenClaw GenPark Dispute Resolver - Schelling point consensus and Dempster-Shafer escrow arbitrator with stake slashing and proportional settlement.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `calculate_schelling_consensus`
- `combine_dempster_shafer_evidence`
- `compute_escrow_settlement`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `calculate_schelling_consensus`
- `combine_dempster_shafer_evidence`
- `compute_escrow_settlement`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
