# ipinfo-mcp

A super simple MCP server for the [IPinfo](https://ipinfo.io) API, starting
with the **Lite** tier (free, unlimited country + ASN lookups).

## Tools

- **`get_ip_info(ip="me")`** — look up country/ASN info for one IP.
  Defaults to `"me"` (your own public IP).
- **`get_bulk_ip_info(ips=[...])`** — look up multiple IPs in one call via
  IPinfo's batch endpoint (up to 1000 per request).

Example Lite response:

```json
{
  "ip": "8.8.8.8",
  "asn": "AS15169",
  "as_name": "Google LLC",
  "as_domain": "google.com",
  "country_code": "US",
  "country": "United States",
  "continent_code": "NA",
  "continent": "North America"
}
```

## Setup

```bash
pip install -r requirements.txt
```

Get a free token at https://ipinfo.io/signup, then set it as an environment
variable (recommended — avoids rate limiting, and IPinfo now requires a
token on most requests):

```bash
export IPINFO_TOKEN=your_token_here
```

## Running locally

```bash
python server.py
```

This starts the server on stdio, ready to be connected to by an MCP client.

## Connecting to Claude Desktop / Claude Code

Add to your MCP config (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ipinfo": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "IPINFO_TOKEN": "your_token_here"
      }
    }
  }
}
```

Restart Claude Desktop (or run `claude mcp add` for Claude Code) and the
`get_ip_info` / `get_bulk_ip_info` tools will be available.

## Notes / next steps

This starts intentionally minimal (Lite tier only: country + ASN, no
city/region/lat-long). Natural next steps if you want to extend it:

- Add a tool for the **Core** or **Plus** tiers (full geolocation, privacy
  flags, etc.) once you have a paid token.
- Add simple in-memory caching to avoid repeat lookups.
- Add input validation for IP format before calling out.
