from server import purchase_places, bookings


def test_purchase_places_updates_points_and_places():
    bookings.clear()

    club = {
        "name": "Test Club",
        "points": "13",
    }

    competition = {
        "name": "Test Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "20",
    }

    success, message = purchase_places(
        club,
        competition,
        5,
    )

    assert success is True
    assert message == "Great-booking complete!"
    assert club["points"] == "8"
    assert competition["numberOfPlaces"] == "15"
