# Zyte Fetch Page Content MCP Server

A Model Context Protocol (MCP) server that extracts clean, LLM-friendly content from any webpage using the [Zyte API](https://www.zyte.com/). Perfect for AI assistants that need to read and understand web content.

## Features

- 🧹 **Clean Content Extraction** - Get main page content 
- 🌐 **Browser Rendering** - Full JavaScript support for dynamic pages
- ⚡ **Configurable Extraction** - Choose between speed (HTTP) or quality (browser rendering)
- 🔒 **Secure** - API keys stored in Docker secrets, runs as non-root user
- 🐳 **Docker-based** - Easy deployment via Docker MCP Toolkit

## Tools Available

The server provides three tools, each using a different extraction method:

| Tool | Description |
|------|-------------|
| `fetch_page_content_from_http_response_body` | Extract from HTTP response (fastest, cheapest) |
| `fetch_page_content_from_browser_html` | Extract from browser with visual features (best quality, default) |
| `fetch_page_content_from_browser_html_only` | Extract from browser HTML only (better for JS-heavy pages) |

### Extraction Methods Explained

| Method | Speed | Cost | Use Case | Returns |
|--------|-------|------|----------|---------|
| **HTTP Response Body** | Fastest | Cheapest | Simple static pages, quick previews | `pageContent` only |
| **Browser HTML** | Medium | Medium | Best quality, visual features included | `pageContent` + `browserHtml` |
| **Browser HTML Only** | Slower | Higher | JavaScript-heavy pages, SPAs | `pageContent` + `browserHtml` |

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- [Zyte API key](https://www.zyte.com/sign-up/) (free tier available)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/zyte-fetch-page-content-mcp-server.git
cd zyte-fetch-page-content-mcp-server
```

### Step 2: Build the Docker Image

```bash
docker build -t zyte-fetch-page-content-mcp-server .
```

### Step 3: Set Your Zyte API Key

```bash
docker mcp secret set ZYTE_API_KEY="your-zyte-api-key-here"
```

Get your API key from [Zyte Dashboard](https://app.zyte.com/o/zyte-api/api-access).

### Step 4: Import the Catalog

```bash
# Create catalogs directory if it doesn't exist
mkdir -p ~/.docker/mcp/catalogs

# Copy catalog file
cp custom.yaml ~/.docker/mcp/catalogs/custom.yaml

# Import the catalog
docker mcp catalog import ~/.docker/mcp/catalogs/custom.yaml
```

### Step 5: Add the Server

```bash
docker mcp server add zyte-fetch-page-content
```

### Step 6: Verify Installation

```bash
# Check server is listed
docker mcp server ls

# Should show:
# zyte-fetch-page-content    -    ✓ done    -    Fetches page content...

# Check tools are available
docker mcp tools ls | grep fetch
```

### Step 7: Configure LLM Client (e.g., Claude Desktop)

Edit your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Ensure it contains:

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    }
  }
}
```

### Step 8: Restart Claude Desktop

Quit Claude Desktop completely (Cmd+Q / Ctrl+Q) and reopen it.

## Usage

Once installed, you can ask Claude to use the tools:

### Basic Usage (Best Quality)

```
Use fetch_page_content_from_browser_html to get content from https://example.com
```

### Fast Extraction (Static Pages)

```
Use fetch_page_content_from_http_response_body to quickly get content from https://example.com
```

### JavaScript-Heavy Pages

```
Use fetch_page_content_from_browser_html_only to extract content from https://example.com
```

### Tool Parameters

All three tools accept a single parameter:

- `url` (required): The URL to fetch content from

**Example:**
```python
fetch_page_content_from_browser_html(url="https://example.com")
```

## Response Format

All tools return raw JSON text from the Zyte API.

### HTTP Response Body Response

```json
{
  "url": "https://example.com",
  "statusCode": 200,
  "pageContent": {
    "itemMain": "Main article content as clean text...",
    "itemSecondary": "Sidebar and navigation content..."
  }
}
```

### Browser HTML Response (with visual features)

```json
{
  "url": "https://example.com",
  "statusCode": 200,
  "browserHtml": "<!DOCTYPE html><html>...</html>",
  "pageContent": {
    "itemMain": "Main article content as clean text...",
    "itemSecondary": "Sidebar and navigation content..."
  }
}
```

### Browser HTML Only Response

```json
{
  "url": "https://example.com",
  "statusCode": 200,
  "browserHtml": "<!DOCTYPE html><html>...</html>",
  "pageContent": {
    "itemMain": "Main article content as clean text...",
    "itemSecondary": "Sidebar and navigation content..."
  }
}
```

## Testing

### Test the Docker Image Directly

```bash
# Test that the server starts
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | docker run --rm -i -e ZYTE_API_KEY="your-key" zyte-fetch-page-content-mcp-server
```

### Test via Docker MCP

```bash
# Test HTTP response body extraction
docker mcp tools call fetch_page_content_from_http_response_body url="https://example.com"

# Test browser HTML extraction (best quality)
docker mcp tools call fetch_page_content_from_browser_html url="https://example.com"

# Test browser HTML only extraction
docker mcp tools call fetch_page_content_from_browser_html_only url="https://example.com"
```

## Troubleshooting

### Server Not Found in Catalog

```bash
# Reimport the catalog
docker mcp catalog rm custom
docker mcp catalog import ~/.docker/mcp/catalogs/custom.yaml
docker mcp server add zyte-fetch-page-content
```

### Tools Not Appearing in Claude

1. Verify server is enabled: `docker mcp server ls`
2. Check tools exist: `docker mcp tools ls | grep fetch`
3. Restart Claude Desktop completely

### API Key Issues

```bash
# Verify secret is set
docker mcp secret ls | grep ZYTE

# Reset the secret
docker mcp secret set ZYTE_API_KEY="your-key"
```

### Configuration Error Response

If you see this response:
```json
{"error": "ZYTE_API_KEY not configured", "type": "config_error"}
```

The API key is not set correctly. Run:
```bash
docker mcp secret set ZYTE_API_KEY="your-actual-key"
```

### Timeout Errors

The default timeout is 120 seconds. If you experience timeouts:
- Use `fetch_page_content_from_http_response_body` for faster results on simple pages
- Consider that complex pages with heavy JavaScript may take longer to render

## How It Works

### Request Flow

```
Claude Desktop
      ↓
MCP Gateway (Docker)
      ↓
Zyte MCP Server (this project)
      ↓
Zyte API (api.zyte.com)
      ↓
Returns JSON with pageContent
```

### Implementation Details

Each tool makes an HTTPS POST request to `https://api.zyte.com/v1/extract` with:
- **Authentication**: HTTP Basic Auth using your Zyte API key
- **Timeout**: 120 seconds
- **Headers**: `Content-Type: application/json`, `Accept-Encoding: gzip`
- **Payload**: URL and extraction options

The tools differ only in their `pageContentOptions.extractFrom` value and whether `browserHtml: true` is included.

## Development

### Local Development

```bash
# Install dependencies
pip install mcp[cli] httpx

# Set API key
export ZYTE_API_KEY="your-key"

# Run server
python zyte_fetch_page_content_server.py
```

### Test MCP Protocol Locally

```bash
# List available tools
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python zyte_fetch_page_content_server.py
```

### Rebuild After Changes

```bash
docker build -t zyte-fetch-page-content-mcp-server .
docker mcp server rm zyte-fetch-page-content
docker mcp server add zyte-fetch-page-content
# Restart Claude Desktop
```

## Security

- API keys are stored in Docker Desktop secrets (never in code)
- Container runs as non-root user
- No sensitive data is logged
- All network requests use HTTPS
- HTTP Basic Auth for API authentication

## Performance Tips

- **For static HTML pages**: Use `fetch_page_content_from_http_response_body` (fastest)
- **For best quality extraction**: Use `fetch_page_content_from_browser_html` (includes visual features)
- **For JavaScript-heavy SPAs**: Use `fetch_page_content_from_browser_html_only`
- **Cost optimization**: HTTP response body extraction is the cheapest option

## Useful Links

- [Zyte API Documentation](https://docs.zyte.com/zyte-api/usage/reference.html)
- [Zyte API Pricing](https://www.zyte.com/pricing/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Docker MCP Toolkit](https://docs.docker.com/desktop/features/mcp-toolkit/)

