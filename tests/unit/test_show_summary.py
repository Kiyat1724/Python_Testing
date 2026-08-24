from server import app


def test_unknown_email_does_not_crash():
    """An unknown email displays an error instead of crashing."""
    client = app.test_client()

    response = client.post(
        "/showSummary",
        data={"email": "unknown@email.com"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Unknown email. Please try again." in response.data
