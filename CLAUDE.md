# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run poe serve      # Run MCP server
uv run poe dev        # Run in development mode (FastMCP dev server)
uv run poe test       # Run all tests
uv run poe check      # Run lint + typecheck
uv run poe format     # Format code with ruff

# Run a single test
uv run pytest tests/test_parks.py::TestGetParkId::test_exact_match -v
```

## Architecture

This is a FastMCP server that proxies the queue-times.com API for theme park wait times.

**parks.py** - Park registry and lookup functions. Contains `PARKS` dict mapping park names to IDs/groups, plus helper functions (`get_park_id`, `get_park_name`, `get_parks_by_group`, `list_all_parks`). Pure functions with no external dependencies.

**server.py** - MCP server with four tools:
- `list_parks` - Returns all parks
- `get_wait_times` - Lookup by name (uses partial matching from parks.py)
- `get_wait_times_by_id` - Lookup by queue-times.com ID
- `get_all_wait_times` - Fetch all parks in a group in parallel

The `format_wait_times()` function transforms API responses into a cleaner structure.

## API Attribution

This project uses data from queue-times.com. Their API requires prominent attribution: "Powered by Queue-Times.com" with a link back to their site.
