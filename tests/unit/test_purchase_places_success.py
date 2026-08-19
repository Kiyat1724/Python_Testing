import server


def test_purchase_places_updates_points_and_places(monkeypatch):
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)

    club = {
        "name": "Test Club",
        "points": "13",
    }

    competition = {
        "name": "Test Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "20",
    }

    success, message = server.purchase_places(
        club,
        competition,
        5,
    )

    assert success is True
    assert message == "Great-booking complete!"
    assert club["points"] == "8"
    assert competition["numberOfPlaces"] == "15"
