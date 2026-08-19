import server


def test_purchase_places_rejects_more_than_12_total(monkeypatch):
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
        "numberOfPlaces": "20",
    }

    success, _ = server.purchase_places(
        club,
        competition,
        8,
    )

    assert success is True

    success, message = server.purchase_places(
        club,
        competition,
        5,
    )

    assert success is False
    assert message == "You cannot book more than 12 places."
