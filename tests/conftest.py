from copy import deepcopy
import pytest
import server


@pytest.fixture(autouse=True)
def isolate_test_data(monkeypatch):
    """
    Isolate application data between tests.

    Regular tests must not modify the real JSON files.
    """

    original_clubs = deepcopy(server.clubs)
    original_competitions = deepcopy(server.competitions)
    original_bookings = deepcopy(server.bookings)

    monkeypatch.setattr(
        server,
        "saveClubs",
        lambda: None,
    )
    monkeypatch.setattr(
        server,
        "saveCompetitions",
        lambda: None,
    )
    monkeypatch.setattr(
        server,
        "saveBookings",
        lambda: None,
    )
    yield

    server.clubs[:] = original_clubs
    server.competitions[:] = original_competitions
    server.bookings[:] = original_bookings
