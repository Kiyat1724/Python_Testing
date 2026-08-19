from server import app, clubs, competitions, bookings


def test_club_cannot_book_more_than_its_points():
    bookings.clear()

    client = app.test_client()

    club = next(
        c for c in clubs
        if c["name"] == "Iron Temple"
    )

    competition = next(
        c for c in competitions
        if c["name"] == "Spring Festival"
    )

    club["points"] = "4"
    competition["numberOfPlaces"] = "25"
    competition["date"] = "2099-03-27 10:00:00"

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Iron Temple",
            "places": "5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Not enough points" in response.data
    assert club["points"] == "4"
    assert competition["numberOfPlaces"] == "25"
