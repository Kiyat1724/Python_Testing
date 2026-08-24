from server import app


def test_points_board_is_displayed():
    """The points board displays all clubs."""
    client = app.test_client()

    response = client.get("/points")

    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data
