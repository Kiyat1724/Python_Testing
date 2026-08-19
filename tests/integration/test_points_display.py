from server import app


def test_points_board_is_displayed():
    client = app.test_client()
    client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"}
    )
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data
