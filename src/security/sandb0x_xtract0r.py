import re
import urllib.parse
from typing import List, Dict

class Sandb0xXtract0r:
    """Monolithic utility for extracting obfuscated payloads and testing WAF rulesets."""

    def __init__(self):
        self.payload_signatures = {
            "sqli": re.compile(r"(?i)(UNION.*SELECT|OR\s+1=1)"),
            "xss": re.compile(r"(?i)(<script>|javascript:)")
        }

    def generate_mutations(self, base_payload: str) -> List[str]:
        """Generates URL-encoded and double-encoded variations to bypass filters."""
        mutations = [
            base_payload,
            urllib.parse.quote(base_payload),
            urllib.parse.quote(urllib.parse.quote(base_payload)),
            base_payload.replace(" ", "/**/")
        ]
        return list(set(mutations))

    def score_request(self, uri: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Scores an incoming request against known malicious signatures."""
        score = 0
        matched_rules = []
        
        decoded_uri = urllib.parse.unquote(uri)
        for sig_name, pattern in self.payload_signatures.items():
            if pattern.search(decoded_uri):
                score += 50
                matched_rules.append(sig_name)
                
        return {
            "risk_score": score,
            "blocked": score >= 50,
            "triggers": matched_rules
        }
