import server


def test_purchase_places_rejects_past_competition(monkeypatch):
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)

    club = {
        "name": "Test Club",
        "points": "20",
    }

    competition = {
        "name": "Past Competition",
        "date": "2020-01-01 10:00:00",
        "numberOfPlaces": "20",
    }

    success, message = server.purchase_places(
        club,
        competition,
        3,
    )

    assert success is False
    assert message == "This competition has already taken place."
