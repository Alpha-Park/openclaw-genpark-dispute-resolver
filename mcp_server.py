# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkDisputeResolver

client = OpenClawGenParkDisputeResolver()

TOOLS = [
    {
        "name": "calculate_schelling_consensus",
        "description": "Calculates Schelling median vote, rewards coherent jurors, and slashes outliers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "juror_votes": {"type": "array", "items": {"type": "object"}},
                "stake_amount": {"type": "number"}
            },
            "required": ["juror_votes"]
        }
    },
    {
        "name": "combine_dempster_shafer_evidence",
        "description": "Combines multi-source conflicting evidence masses via Dempster's rule.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "evidence_masses": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["evidence_masses"]
        }
    },
    {
        "name": "compute_escrow_settlement",
        "description": "Calculates exact proportional escrow disbursement between buyer and seller.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "buyer_claim": {"type": "number"},
                "seller_claim": {"type": "number"},
                "total_escrow_usd": {"type": "number"},
                "buyer_support_prob": {"type": "number"}
            },
            "required": ["buyer_claim", "seller_claim", "total_escrow_usd", "buyer_support_prob"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "calculate_schelling_consensus":
            res = client.calculate_schelling_consensus(args["juror_votes"], args.get("stake_amount", 100.0))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "combine_dempster_shafer_evidence":
            res = client.combine_dempster_shafer_evidence(args["evidence_masses"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_escrow_settlement":
            res = client.compute_escrow_settlement(args["buyer_claim"], args["seller_claim"], args["total_escrow_usd"], args["buyer_support_prob"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)
                continue
            if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}), flush=True)
                continue
            # JSON-RPC notifications never receive a response or execute request-only tools.
            if "id" not in req:
                continue
            if req["method"] == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": 'openclaw-genpark-dispute-resolver', "version": "1.0.0"}
                }}), flush=True)
                continue
            if req["method"] == "ping":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}), flush=True)
                continue
            if req["method"] not in ("tools/list", "tools/call"):
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            if req["method"] == "tools/call":
                params = req.get("params")
                if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict) or params.get("name") not in ('calculate_schelling_consensus', 'combine_dempster_shafer_evidence', 'compute_escrow_settlement'):
                    print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": "Unknown tool or invalid arguments"}}), flush=True)
                    continue
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
