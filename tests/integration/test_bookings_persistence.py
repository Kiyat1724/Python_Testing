import json

import server


def test_booking_is_saved_in_bookings_json(
    tmp_path,
    monkeypatch,
):
    server.bookings.clear()

    bookings_file = tmp_path / "bookings.json"

    def save_test_bookings():
        with open(bookings_file, "w") as file:
            json.dump(
                {"bookings": server.bookings},
                file,
                indent=4,
            )

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
        save_test_bookings,
    )

    club = {
        "name": "Test Club",
        "points": "20",
    }

    competition = {
        "name": "Test Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "20",
    }

    success, message = server.purchase_places(
        club,
        competition,
        4,
    )

    assert success is True
    assert message == "Great-booking complete!"

    with open(bookings_file) as file:
        saved_bookings = json.load(file)["bookings"]

    assert saved_bookings == [
        {
            "club": "Test Club",
            "competition": "Test Competition",
            "places": 4,
        }
    ]