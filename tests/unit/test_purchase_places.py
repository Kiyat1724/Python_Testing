import server


def test_purchase_places_updates_points_and_places(monkeypatch):
    """A valid booking updates points and available places."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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


def test_purchase_places_rejects_more_than_12_total(monkeypatch):
    """A club cannot book more than 12 places in total."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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


def test_purchase_places_rejects_when_capacity_is_insufficient(monkeypatch):
    """A booking is rejected when the competition has too few places."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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


def test_purchase_places_rejects_zero(monkeypatch):
    """A booking of zero places is rejected."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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
    """A booking with a negative quantity is rejected."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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


def test_purchase_places_rejects_past_competition(monkeypatch):
    """A booking cannot be made for a past competition."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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


def test_purchase_places_rejects_when_points_are_insufficient(monkeypatch):
    """A booking is rejected when the club has too few points."""
    server.bookings.clear()

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", lambda: None)

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