from server import app, clubs, competitions, bookings


def test_club_cannot_book_more_places_than_available():
    bookings.clear()

    client = app.test_client()

    club = next(
        c for c in clubs
        if c["name"] == "Simply Lift"
    )

    competition = next(
        c for c in competitions
        if c["name"] == "Fall Classic"
    )

    club["points"] = "13"
    competition["numberOfPlaces"] = "5"
    competition["date"] = "2099-10-22 13:30:00"

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "6",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Not enough places available." in response.data
    assert competition["numberOfPlaces"] == "5"
    assert club["points"] == "13"
