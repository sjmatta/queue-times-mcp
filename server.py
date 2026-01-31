"""Queue-Times MCP Server - Theme park wait times from queue-times.com."""

import asyncio

import httpx
from fastmcp import FastMCP

from parks import (
    get_park_id,
    get_park_name,
    get_parks_by_group,
    list_all_parks,
)

mcp = FastMCP("queue-times")

API_BASE = "https://queue-times.com/parks"


async def fetch_wait_times(park_id: int) -> dict:
    """Fetch wait times from queue-times.com API."""
    url = f"{API_BASE}/{park_id}/queue_times.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.json()


def format_wait_times(park_name: str, data: dict) -> dict:
    """Format API response into a cleaner structure."""
    lands = []
    for land in data.get("lands", []):
        rides = []
        for ride in land.get("rides", []):
            rides.append(
                {
                    "name": ride.get("name"),
                    "wait_time": ride.get("wait_time"),
                    "is_open": ride.get("is_open", False),
                }
            )
        if rides:
            lands.append(
                {
                    "name": land.get("name"),
                    "rides": rides,
                }
            )
    return {
        "park": park_name,
        "lands": lands,
    }


@mcp.tool()
def list_parks() -> list[dict]:
    """List all available theme parks with their IDs and groups.

    Returns a list of parks including Disney, Universal, SeaWorld, and other parks
    with their queue-times.com IDs and operator groups.
    """
    return list_all_parks()


@mcp.tool()
async def get_wait_times(park_name: str) -> dict:
    """Get current wait times for a theme park by name.

    Args:
        park_name: Name of the park (e.g., "Kennywood", "Magic Kingdom", "Disneyland").
                   Partial matches are supported (e.g., "magic" matches "Magic Kingdom").

    Returns:
        Current wait times organized by land/area with ride names, wait times in minutes,
        and open/closed status.
    """
    park_id = get_park_id(park_name)
    if park_id is None:
        available = [p["name"] for p in list_all_parks()]
        return {
            "error": f"Park '{park_name}' not found",
            "available_parks": available,
        }

    resolved_name = get_park_name(park_id) or park_name
    data = await fetch_wait_times(park_id)
    return format_wait_times(resolved_name, data)


@mcp.tool()
async def get_wait_times_by_id(park_id: int) -> dict:
    """Get current wait times for a theme park by its queue-times.com ID.

    Args:
        park_id: The queue-times.com park ID (e.g., 312 for Kennywood, 6 for Magic Kingdom).

    Returns:
        Current wait times organized by land/area with ride names, wait times in minutes,
        and open/closed status.
    """
    park_name = get_park_name(park_id)
    if park_name is None:
        park_name = f"Park {park_id}"

    data = await fetch_wait_times(park_id)
    return format_wait_times(park_name, data)


@mcp.tool()
async def get_all_wait_times(group: str) -> dict:
    """Get wait times for all parks in a group (fetches in parallel).

    Args:
        group: The park operator group. Options: "disney", "universal", "seaworld", "parques_reunidos"

    Returns:
        Wait times for all parks in the specified group.
    """
    parks = get_parks_by_group(group)
    if not parks:
        return {
            "error": f"Group '{group}' not found",
            "available_groups": ["disney", "universal", "seaworld", "parques_reunidos"],
        }

    async def fetch_park(name: str, park_id: int) -> dict:
        try:
            data = await fetch_wait_times(park_id)
            return format_wait_times(name, data)
        except Exception as e:
            return {"park": name, "error": str(e)}

    tasks = [fetch_park(name, park_id) for name, park_id in parks.items()]
    results = await asyncio.gather(*tasks)

    return {
        "group": group,
        "parks": results,
    }


if __name__ == "__main__":
    mcp.run()
