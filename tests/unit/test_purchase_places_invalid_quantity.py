import server


def test_purchase_places_rejects_zero(monkeypatch):
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

    success, message = server.purchase_places(
        club,
        competition,
        0,
    )

    assert success is False
    assert message == "You must book at least one place."


def test_purchase_places_rejects_negative_value(monkeypatch):
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

    success, message = server.purchase_places(
        club,
        competition,
        -3,
    )

    assert success is False
    assert message == "You must book at least one place."
