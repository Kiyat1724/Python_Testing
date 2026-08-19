from server import app, clubs, competitions, bookings


def test_points_are_updated_after_booking():
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

    # État contrôlé pour ce test
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