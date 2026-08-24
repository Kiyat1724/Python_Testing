from server import app


def test_user_can_login_view_points_and_logout():
    """A secretary can log in, view the points board, and log out."""
    client = app.test_client()

    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"john@simplylift.co" in response.data

    response = client.get(
        "/points",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data

    response = client.get(
        "/logout",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"GUDLFT Registration" in response.data
