import json

import server
from server import saveBookings, saveClubs, saveCompetitions


def test_save_clubs(tmp_path, monkeypatch):
    """saveClubs writes club data to clubs.json."""
    monkeypatch.chdir(tmp_path)

    server.clubs[:] = [
        {
            "name": "Test Club",
            "email": "test@example.com",
            "points": "10",
        }
    ]

    saveClubs()

    with open("clubs.json") as file:
        saved_data = json.load(file)

    assert saved_data == {
        "clubs": [
            {
                "name": "Test Club",
                "email": "test@example.com",
                "points": "10",
            }
        ]
    }


def test_save_competitions(tmp_path, monkeypatch):
    """saveCompetitions writes competition data to competitions.json."""
    monkeypatch.chdir(tmp_path)

    server.competitions[:] = [
        {
            "name": "Test Competition",
            "date": "2099-01-01 10:00:00",
            "numberOfPlaces": "20",
        }
    ]

    saveCompetitions()

    with open("competitions.json") as file:
        saved_data = json.load(file)

    assert saved_data == {
        "competitions": [
            {
                "name": "Test Competition",
                "date": "2099-01-01 10:00:00",
                "numberOfPlaces": "20",
            }
        ]
    }


def test_save_bookings(tmp_path, monkeypatch):
    """saveBookings writes booking data to bookings.json."""
    monkeypatch.chdir(tmp_path)

    server.bookings[:] = [
        {
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 4,
        }
    ]

    saveBookings()

    with open("bookings.json") as file:
        saved_data = json.load(file)

    assert saved_data == {
        "bookings": [
            {
                "club": "Test Club",
                "competition": "Test Competition",
                "places": 4,
            }
        ]
    }
