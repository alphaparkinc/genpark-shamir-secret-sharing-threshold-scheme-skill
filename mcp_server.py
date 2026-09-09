"""MCP Server for Shamir Secret Sharing Skill."""
import json
import sys
from client import ShamirSecretSharing

def main():
    sss = ShamirSecretSharing()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [
                            {
                                "name": "split_secret",
                                "description": "Split secret into n threshold shares requiring k to recover",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "secret": {"type": "integer"},
                                        "threshold_k": {"type": "integer"},
                                        "total_shares_n": {"type": "integer"}
                                    },
                                    "required": ["secret", "threshold_k", "total_shares_n"]
                                }
                            },
                            {
                                "name": "recover_secret",
                                "description": "Reconstruct secret from k shares",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "shares": {"type": "array", "items": {"type": "array"}}
                                    },
                                    "required": ["shares"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "split_secret":
                    shares = sss.split_secret(args["secret"], args["threshold_k"], args["total_shares_n"])
                    out = {"shares": shares}
                else:
                    shares = [tuple(s) for s in args["shares"]]
                    out = {"secret": sss.reconstruct_secret(shares)}
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(out)}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
