import pytest
import asyncio
from src.security.honeyroot_honeypot import HoneyRootHoneypot

@pytest.mark.asyncio
async def test_honeypot_connection_logging():
    pot = HoneyRootHoneypot()
    session = await pot.log_connection("192.168.1.100", {"user": "root", "pass": "toor"})
    
    assert session["ip"] == "192.168.1.100"
    assert session["threat_level"] == "critical"
    assert session["vt_analysis"]["status"] == "flagged"
