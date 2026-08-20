import json
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
)


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def loadClubs():
    with open("clubs.json") as c:
        return json.load(c)["clubs"]


def loadCompetitions():
    with open("competitions.json") as comps:
        return json.load(comps)["competitions"]


def loadBookings():
    with open("bookings.json") as bookings_file:
        return json.load(bookings_file)["bookings"]


app = Flask(__name__)
app.secret_key = "something_special"


clubs = loadClubs()
competitions = loadCompetitions()
bookings = loadBookings()


def saveClubs():
    with open("clubs.json", "w") as c:
        json.dump({"clubs": clubs}, c, indent=4)


def saveCompetitions():
    with open("competitions.json", "w") as comps:
        json.dump({"competitions": competitions}, comps, indent=4)


def saveBookings():
    with open("bookings.json", "w") as bookings_file:
        json.dump(
            {"bookings": bookings},
            bookings_file,
            indent=4,
        )


def get_already_booked(club_name, competition_name):
    """
    Return the total number of places already booked
    by one club for one competition.
    """
    return sum(
        booking["places"]
        for booking in bookings
        if booking["club"] == club_name
        and booking["competition"] == competition_name
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = next(
        (
            club
            for club in clubs
            if club["email"] == request.form["email"]
        ),
        None,
    )

    if club is None:
        flash("Unknown email. Please try again.")
        return render_template("index.html")

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        now=datetime.now().strftime(DATE_FORMAT),
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = next(
        c for c in clubs
        if c["name"] == club
    )

    foundCompetition = next(
        c for c in competitions
        if c["name"] == competition
    )

    competition_date = datetime.strptime(
        foundCompetition["date"],
        DATE_FORMAT,
    )

    if competition_date < datetime.now():
        flash("This competition has already taken place.")
        return render_template(
            "welcome.html",
            club=foundClub,
            competitions=competitions,
            now=datetime.now().strftime(DATE_FORMAT),
        )

    already_booked = get_already_booked(
        foundClub["name"],
        foundCompetition["name"],
    )

    max_places = min(
        12 - already_booked,
        int(foundCompetition["numberOfPlaces"]),
        int(foundClub["points"]),
    )

    max_places = max(max_places, 0)

    return render_template(
        "booking.html",
        club=foundClub,
        competition=foundCompetition,
        max_places=max_places,
    )


def purchase_places(club, competition, places_required):
    """
    Validate a booking and update application data.

    Returns:
        (True, message) when the booking succeeds.
        (False, error_message) when a business rule fails.
    """
    club_points = int(club["points"])
    competition_places = int(competition["numberOfPlaces"])

    already_booked = get_already_booked(
        club["name"],
        competition["name"],
    )

    if places_required <= 0:
        return False, "You must book at least one place."

    if already_booked + places_required > 12:
        return False, "You cannot book more than 12 places."

    competition_date = datetime.strptime(
        competition["date"],
        DATE_FORMAT,
    )

    if competition_date < datetime.now():
        return False, "This competition has already taken place."

    if places_required > competition_places:
        return False, "Not enough places available."

    if places_required > club_points:
        return False, "Not enough points."

    competition["numberOfPlaces"] = str(
        competition_places - places_required
    )

    club["points"] = str(
        club_points - places_required
    )

    bookings.append(
        {
            "club": club["name"],
            "competition": competition["name"],
            "places": places_required,
        }
    )

    saveClubs()
    saveCompetitions()
    saveBookings()

    return True, "Great-booking complete!"


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = next(
        c for c in competitions
        if c["name"] == request.form["competition"]
    )

    club = next(
        c for c in clubs
        if c["name"] == request.form["club"]
    )

    places_required = int(request.form["places"])

    success, message = purchase_places(
        club,
        competition,
        places_required,
    )

    flash(message)

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        now=datetime.now().strftime(DATE_FORMAT),
    )


@app.route("/points")
def displayPoints():
    return render_template(
        "points.html",
        clubs=clubs,
    )


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
