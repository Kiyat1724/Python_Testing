import json

import server


def test_load_clubs(tmp_path, monkeypatch):
    """loadClubs returns clubs stored in clubs.json."""
    test_file = tmp_path / "clubs.json"

    test_data = {
        "clubs": [
            {
                "name": "Test Club",
                "email": "test@example.com",
                "points": "10",
            }
        ]
    }

    test_file.write_text(
        json.dumps(test_data),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    clubs = server.loadClubs()

    assert clubs == test_data["clubs"]


def test_load_competitions(tmp_path, monkeypatch):
    """loadCompetitions returns competitions stored in competitions.json."""
    test_file = tmp_path / "competitions.json"

    test_data = {
        "competitions": [
            {
                "name": "Test Competition",
                "date": "2099-01-01 10:00:00",
                "numberOfPlaces": "20",
            }
        ]
    }

    test_file.write_text(
        json.dumps(test_data),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    competitions = server.loadCompetitions()

    assert competitions == test_data["competitions"]


def test_load_bookings(tmp_path, monkeypatch):
    """loadBookings returns bookings stored in bookings.json."""
    test_file = tmp_path / "bookings.json"

    test_data = {
        "bookings": [
            {
                "club": "Test Club",
                "competition": "Test Competition",
                "places": 4,
            }
        ]
    }

    test_file.write_text(
        json.dumps(test_data),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    bookings = server.loadBookings()

    assert bookings == test_data["bookings"]