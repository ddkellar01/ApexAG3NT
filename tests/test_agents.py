import pytest
from unittest.mock import patch
from src.agents.fixflow_remediator import FixFlowRemediator
from src.security.sandb0x_xtract0r import Sandb0xXtract0r

@pytest.mark.asyncio
async def test_fixflow_alert_fetching():
    agent = FixFlowRemediator("darnellwashingtonjr94-art/shannon")
    alerts = await agent.fetch_open_alerts()
    assert len(alerts) > 0
    assert "vulnerability" in alerts[0]

def test_sandb0x_xtract0r_mutations():
    extractor = Sandb0xXtract0r()
    mutations = extractor.generate_mutations("<script>alert(1)</script>")
    
    assert len(mutations) >= 3
    assert "%3Cscript%3E" in mutations  # Verifies URL encoding happened

def test_sandb0x_xtract0r_scoring():
    extractor = Sandb0xXtract0r()
    safe_req = extractor.score_request("/api/v1/health", {})
    assert safe_req["blocked"] is False
    
    malicious_req = extractor.score_request("/search?q=UNION+SELECT+1,2", {})
    assert malicious_req["blocked"] is True
    assert "sqli" in malicious_req["triggers"]
