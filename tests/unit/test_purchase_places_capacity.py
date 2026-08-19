import server


def test_purchase_places_rejects_when_capacity_is_insufficient(monkeypatch):
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)

    club = {
        "name": "Test Club",
        "points": "20",
    }

    competition = {
        "name": "Test Competition",
        "date": "2099-01-01 10:00:00",
        "numberOfPlaces": "5",
    }

    success, message = server.purchase_places(
        club,
        competition,
        6,
    )

    assert success is False
    assert message == "Not enough places available."
    assert competition["numberOfPlaces"] == "5"
