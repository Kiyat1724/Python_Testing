import json

import server


def test_booking_is_saved_in_json_files(tmp_path, monkeypatch):
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
