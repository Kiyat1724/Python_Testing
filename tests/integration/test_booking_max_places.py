from server import app


def test_club_cannot_book_more_than_12_places():
    client = app.test_client()

    client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"}
    )

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13"
        },
        follow_redirects=True
    )

    assert b"You cannot book more than 12 places." in response.data