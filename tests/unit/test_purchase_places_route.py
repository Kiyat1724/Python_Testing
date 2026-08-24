from server import app, clubs, competitions, bookings


def test_route_rejects_more_than_12_places():
    """The purchase route rejects a booking above 12 places."""
    bookings.clear()

    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cannot book more than 12 places." in response.data


def test_route_rejects_booking_above_club_points():
    """The purchase route rejects a booking above the club balance."""
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


def test_route_rejects_booking_above_competition_capacity():
    """The purchase route rejects a booking above available capacity."""
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


def test_route_updates_points_and_places():
    """A successful route booking updates club points and capacity."""
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
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "3",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert club["points"] == "10"
    assert competition["numberOfPlaces"] == "10"
