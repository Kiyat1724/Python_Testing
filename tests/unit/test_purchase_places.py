import json
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
    """A booking is rejected when too few places are available."""
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


def test_purchase_places_saves_booking_in_json(tmp_path, monkeypatch):
    """A successful booking is persisted in bookings.json."""
    server.bookings.clear()

    bookings_file = tmp_path / "bookings.json"

    def save_test_bookings():
        with open(bookings_file, "w") as file:
            json.dump(
                {"bookings": server.bookings},
                file,
                indent=4,
            )

    monkeypatch.setattr(server, "saveClubs", lambda: None)
    monkeypatch.setattr(server, "saveCompetitions", lambda: None)
    monkeypatch.setattr(server, "saveBookings", save_test_bookings)

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


def test_purchase_places_persists_points_and_places(tmp_path, monkeypatch):
    """A successful booking persists updated points and places."""
    server.bookings.clear()

    clubs_file = tmp_path / "clubs.json"
    competitions_file = tmp_path / "competitions.json"

    club = next(
        c for c in server.clubs
        if c["name"] == "Simply Lift"
    )

    competition = next(
        c for c in server.competitions
        if c["name"] == "Fall Classic"
    )

    original_points = club["points"]
    original_places = competition["numberOfPlaces"]
    original_date = competition["date"]

    try:
        club["points"] = "13"
        competition["numberOfPlaces"] = "13"
        competition["date"] = "2099-10-22 13:30:00"

        def save_test_clubs():
            with open(clubs_file, "w") as file:
                json.dump(
                    {"clubs": server.clubs},
                    file,
                    indent=4,
                )

        def save_test_competitions():
            with open(competitions_file, "w") as file:
                json.dump(
                    {"competitions": server.competitions},
                    file,
                    indent=4,
                )

        monkeypatch.setattr(
            server,
            "saveClubs",
            save_test_clubs,
        )
        monkeypatch.setattr(
            server,
            "saveCompetitions",
            save_test_competitions,
        )
        monkeypatch.setattr(
            server,
            "saveBookings",
            lambda: None,
        )

        success, message = server.purchase_places(
            club,
            competition,
            3,
        )

        assert success is True
        assert message == "Great-booking complete!"

        with open(clubs_file) as file:
            saved_clubs = json.load(file)["clubs"]

        with open(competitions_file) as file:
            saved_competitions = json.load(file)["competitions"]

        saved_club = next(
            c for c in saved_clubs
            if c["name"] == "Simply Lift"
        )

        saved_competition = next(
            c for c in saved_competitions
            if c["name"] == "Fall Classic"
        )

        assert saved_club["points"] == "10"
        assert saved_competition["numberOfPlaces"] == "10"

    finally:
        club["points"] = original_points
        competition["numberOfPlaces"] = original_places
        competition["date"] = original_date
        server.bookings.clear()
