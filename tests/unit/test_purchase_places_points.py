import server


def test_purchase_places_rejects_when_points_are_insufficient(monkeypatch):
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)

    club = {
        "name": "Test Club",
        "points": "3",
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

    assert success is False
    assert message == "Not enough points."
    assert club["points"] == "3"
