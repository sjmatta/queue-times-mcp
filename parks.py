"""Park definitions for queue-times.com API."""

from typing import TypedDict


class ParkInfo(TypedDict):
    id: int
    group: str


# Parks organized by operator group
PARKS: dict[str, ParkInfo] = {
    # Disney Parks
    "Magic Kingdom": {"id": 6, "group": "disney"},
    "Epcot": {"id": 5, "group": "disney"},
    "Hollywood Studios": {"id": 7, "group": "disney"},
    "Animal Kingdom": {"id": 8, "group": "disney"},
    "Disneyland": {"id": 16, "group": "disney"},
    "Disney California Adventure": {"id": 17, "group": "disney"},
    "Disneyland Paris": {"id": 4, "group": "disney"},
    "Walt Disney Studios Paris": {"id": 28, "group": "disney"},
    "Hong Kong Disneyland": {"id": 31, "group": "disney"},
    "Shanghai Disney": {"id": 30, "group": "disney"},
    "Tokyo Disneyland": {"id": 274, "group": "disney"},
    "Tokyo DisneySea": {"id": 275, "group": "disney"},
    # Universal Parks
    "Universal Studios Hollywood": {"id": 66, "group": "universal"},
    "Universal Studios Orlando": {"id": 65, "group": "universal"},
    "Islands of Adventure": {"id": 64, "group": "universal"},
    "Volcano Bay": {"id": 67, "group": "universal"},
    "Epic Universe": {"id": 334, "group": "universal"},
    # SeaWorld Parks
    "Busch Gardens Williamsburg": {"id": 23, "group": "seaworld"},
    # Parques Reunidos
    "Kennywood": {"id": 312, "group": "parques_reunidos"},
}

# Reverse lookup: ID -> park name
PARK_IDS = {info["id"]: name for name, info in PARKS.items()}


def get_park_id(name: str) -> int | None:
    """Get park ID by name (case-insensitive partial match)."""
    name_lower = name.lower()
    # Exact match first
    for park_name, info in PARKS.items():
        if park_name.lower() == name_lower:
            return info["id"]
    # Partial match
    for park_name, info in PARKS.items():
        if name_lower in park_name.lower():
            return info["id"]
    return None


def get_park_name(park_id: int) -> str | None:
    """Get park name by ID."""
    return PARK_IDS.get(park_id)


def get_parks_by_group(group: str) -> dict[str, int]:
    """Get all parks in a group (disney, universal, seaworld, parques_reunidos)."""
    group_lower = group.lower()
    return {name: info["id"] for name, info in PARKS.items() if info["group"] == group_lower}


def list_all_parks() -> list[dict]:
    """List all available parks with their IDs and groups."""
    return [
        {"name": name, "id": info["id"], "group": info["group"]} for name, info in PARKS.items()
    ]
