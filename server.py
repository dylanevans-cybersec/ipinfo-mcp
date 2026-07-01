"""
IPInfo - IP Geolocation and ASN lookup

This is a super simple MCP server for the IPinfo API — starting with IPinfo Lite.

IPinfo Lite is IPinfo's free, unlimited tier. It returns country + ASN
level info for an IP (no city/region/lat-long — that's the Core/Plus tiers).

Docs: https://ipinfo.io/developers/lite-api

Setup:
    pip install mcp httpx
    export IPINFO_TOKEN=your_token_here   # optional but recommended, see README

Run (for local testing over stdio):
    python server.py
"""

import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

IPINFO_BASE_URL = "https://api.ipinfo.io"
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN", "")

mcp = FastMCP("ipinfo")


async def _get(path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Make a GET request against the IPinfo API and return parsed JSON."""
    params = dict(params or {})
    if IPINFO_TOKEN:
        params["token"] = IPINFO_TOKEN

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{IPINFO_BASE_URL}{path}", params=params)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_ip_info(ip: str = "me") -> dict[str, Any]:
    """Look up country and ASN info for an IP address using IPinfo.

    Args:
        ip: The IPv4 or IPv6 address to look up. Defaults to "me", which
            looks up the caller's own public IP address.

    Returns:
        A dict with fields like ip, asn, as_name, as_domain, country_code,
        country, continent_code, and continent.
    """
    return await _get(f"/lite/{ip}")


@mcp.tool()
async def get_bulk_ip_info(ips: list[str]) -> dict[str, Any]:
    """Look up country and ASN info for multiple IP addresses at once.

    Uses IPinfo's batch/lite endpoint (free tier, up to 1000 IPs per call).

    Args:
        ips: A list of IPv4/IPv6 addresses to look up.

    Returns:
        A dict mapping each requested "lite/<ip>" key to its lookup result.
    """
    params = {"token": IPINFO_TOKEN} if IPINFO_TOKEN else {}
    payload = [f"lite/{ip}" for ip in ips]

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            f"{IPINFO_BASE_URL}/batch/lite", params=params, json=payload
        )
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
