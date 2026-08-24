from server import app, competitions, bookings


def test_cannot_book_past_competition():
    """The booking page is unavailable for a past competition."""
    bookings.clear()

    competition = next(
        c for c in competitions
        if c["name"] == "Spring Festival"
    )

    competition["date"] = "2020-03-27 10:00:00"
    competition["numberOfPlaces"] = "25"

    client = app.test_client()

    response = client.get(
        "/book/Spring Festival/Simply Lift",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"This competition has already taken place." in response.data
