"""Tests for server.py - format_wait_times and error handling."""

import pytest

from server import format_wait_times, get_all_wait_times, get_wait_times


class TestFormatWaitTimes:
    """Tests for format_wait_times() - pure data transformation."""

    def test_empty_lands(self):
        result = format_wait_times("Test Park", {"lands": []})
        assert result == {"park": "Test Park", "lands": []}

    def test_filters_empty_rides(self):
        data = {
            "lands": [
                {"name": "Empty Land", "rides": []},
                {
                    "name": "Fun Land",
                    "rides": [{"name": "Roller Coaster", "wait_time": 30, "is_open": True}],
                },
            ]
        }
        result = format_wait_times("Test Park", data)
        assert len(result["lands"]) == 1
        assert result["lands"][0]["name"] == "Fun Land"

    def test_extracts_ride_fields(self):
        data = {
            "lands": [
                {
                    "name": "Main Area",
                    "rides": [
                        {
                            "name": "The Ride",
                            "wait_time": 45,
                            "is_open": True,
                            "extra_field": "ignored",
                        }
                    ],
                }
            ]
        }
        result = format_wait_times("Test Park", data)
        ride = result["lands"][0]["rides"][0]
        assert ride == {"name": "The Ride", "wait_time": 45, "is_open": True}
        assert "extra_field" not in ride

    def test_defaults_is_open_to_false(self):
        data = {"lands": [{"name": "Area", "rides": [{"name": "Ride", "wait_time": 0}]}]}
        result = format_wait_times("Test Park", data)
        assert result["lands"][0]["rides"][0]["is_open"] is False

    def test_missing_lands_key(self):
        result = format_wait_times("Test Park", {})
        assert result == {"park": "Test Park", "lands": []}


class TestGetWaitTimesErrorHandling:
    """Tests for get_wait_times() error paths without network calls."""

    @pytest.mark.asyncio
    async def test_unknown_park_returns_error(self):
        result = await get_wait_times("Neverland Park")  # type: ignore[operator]
        assert "error" in result
        assert "Neverland Park" in result["error"]
        assert "available_parks" in result
        assert isinstance(result["available_parks"], list)
        assert len(result["available_parks"]) > 0


class TestGetAllWaitTimesErrorHandling:
    """Tests for get_all_wait_times() error paths without network calls."""

    @pytest.mark.asyncio
    async def test_invalid_group_returns_error(self):
        result = await get_all_wait_times("invalid_group")  # type: ignore[operator]
        assert "error" in result
        assert "invalid_group" in result["error"]
        assert "available_groups" in result
        assert "disney" in result["available_groups"]
        assert "universal" in result["available_groups"]
