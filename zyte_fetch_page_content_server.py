#!/usr/bin/env python3
"""
Zyte Fetch Page Content MCP Server - Fetches page content using Zyte API with configurable extraction sources.
"""
import os
import sys
import logging
import json
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("zyte-fetch-page-content-server")

# Initialize MCP server
mcp = FastMCP("zyte-fetch-page-content")

# Configuration
ZYTE_API_URL = "https://api.zyte.com/v1/extract"
ZYTE_API_KEY = os.environ.get("ZYTE_API_KEY", "")


@mcp.tool()
async def fetch_page_content_from_http_response_body(url: str = "") -> str:
    """Extract page content from HTTP response body (fastest, cheapest method)."""
    if not ZYTE_API_KEY:
        error_data = {"error": "ZYTE_API_KEY not configured", "type": "config_error"}
        return json.dumps(error_data)

    payload = {
        "url": url,
        "pageContent": True,
        "pageContentOptions": {"extractFrom": "httpResponseBody"}
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            ZYTE_API_URL,
            auth=(ZYTE_API_KEY, ""),
            headers={
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip"
            },
            json=payload
        )
        return response.text


@mcp.tool()
async def fetch_page_content_from_browser_html(url: str = "") -> str:
    """Extract page content from browser HTML with visual features (default and best quality method)."""
    if not ZYTE_API_KEY:
        error_data = {"error": "ZYTE_API_KEY not configured", "type": "config_error"}
        return json.dumps(error_data)

    payload = {
        "url": url,
        "pageContent": True,
        "browserHtml": True,
        "pageContentOptions": {"extractFrom": "browserHtml"}
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            ZYTE_API_URL,
            auth=(ZYTE_API_KEY, ""),
            headers={
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip"
            },
            json=payload
        )
        return response.text


@mcp.tool()
async def fetch_page_content_from_browser_html_only(url: str = "") -> str:
    """Extract page content from browser HTML only (better for JS-heavy pages)."""
    if not ZYTE_API_KEY:
        error_data = {"error": "ZYTE_API_KEY not configured", "type": "config_error"}
        return json.dumps(error_data)

    payload = {
        "url": url,
        "pageContent": True,
        "browserHtml": True,
        "pageContentOptions": {"extractFrom": "browserHtmlOnly"}
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            ZYTE_API_URL,
            auth=(ZYTE_API_KEY, ""),
            headers={
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip"
            },
            json=payload
        )
        return response.text


# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting Zyte Fetch Page Content MCP server...")
    
    if not ZYTE_API_KEY:
        logger.warning("ZYTE_API_KEY not set in environment")
    else:
        logger.info("ZYTE_API_KEY configured from environment")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)