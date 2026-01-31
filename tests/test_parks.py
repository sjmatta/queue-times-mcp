"""Tests for parks.py helper functions."""

from parks import get_park_id, get_park_name, get_parks_by_group, list_all_parks


class TestGetParkId:
    """Tests for get_park_id() - case-insensitive partial matching."""

    def test_exact_match(self):
        assert get_park_id("Kennywood") == 312

    def test_case_insensitive(self):
        assert get_park_id("kennywood") == 312
        assert get_park_id("KENNYWOOD") == 312

    def test_partial_match(self):
        assert get_park_id("magic") == 6  # Magic Kingdom

    def test_unknown_park(self):
        assert get_park_id("Neverland") is None

    def test_exact_match_takes_priority(self):
        # "Disneyland" should match exactly, not "Disneyland Paris"
        assert get_park_id("Disneyland") == 16


class TestGetParkName:
    """Tests for get_park_name() - reverse lookup by ID."""

    def test_known_id(self):
        assert get_park_name(312) == "Kennywood"
        assert get_park_name(6) == "Magic Kingdom"

    def test_unknown_id(self):
        assert get_park_name(9999) is None


class TestGetParksByGroup:
    """Tests for get_parks_by_group() - group filtering."""

    def test_valid_group(self):
        parks = get_parks_by_group("disney")
        assert isinstance(parks, dict)
        assert len(parks) > 0
        assert "Magic Kingdom" in parks
        assert parks["Magic Kingdom"] == 6

    def test_case_insensitive(self):
        assert get_parks_by_group("Disney") == get_parks_by_group("disney")
        assert get_parks_by_group("UNIVERSAL") == get_parks_by_group("universal")

    def test_unknown_group(self):
        assert get_parks_by_group("nonexistent") == {}


class TestListAllParks:
    """Tests for list_all_parks() - structure validation."""

    def test_returns_list(self):
        parks = list_all_parks()
        assert isinstance(parks, list)
        assert len(parks) > 0

    def test_entry_structure(self):
        parks = list_all_parks()
        for park in parks:
            assert "name" in park
            assert "id" in park
            assert "group" in park
            assert isinstance(park["name"], str)
            assert isinstance(park["id"], int)
            assert isinstance(park["group"], str)

    def test_contains_known_parks(self):
        parks = list_all_parks()
        names = [p["name"] for p in parks]
        assert "Kennywood" in names
        assert "Magic Kingdom" in names
