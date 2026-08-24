from server import app, clubs, competitions, bookings


def test_user_can_complete_booking_journey():
    """A secretary can log in, open a booking page, and book places."""
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
    competition["numberOfPlaces"] = "13"
    competition["date"] = "2099-10-22 13:30:00"

    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    response = client.get(
        "/book/Fall Classic/Simply Lift",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"How many places?" in response.data

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "3",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    assert club["points"] == "10"
    assert competition["numberOfPlaces"] == "10"

    assert any(
        booking["club"] == "Simply Lift"
        and booking["competition"] == "Fall Classic"
        and booking["places"] == 3
        for booking in bookings
    )
