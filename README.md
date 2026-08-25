# GUDLFT Registration

## Project Overview

GUDLFT Registration is a lightweight Flask proof-of-concept application for managing competition bookings between sports clubs.

The objective of this project is to improve an existing Python web application by identifying and fixing bugs, implementing business rules, improving data persistence, and building a structured automated testing strategy.

The project focuses particularly on software quality, debugging, testing, validation of business requirements, data consistency, and performance testing.

## Main Features

Club secretaries can:

- log in using their club email address;
- view their current points balance;
- view available competitions;
- book places for future competitions;
- view the points balance of all clubs.

The application prevents invalid bookings by applying validation rules both in the user interface and in the backend.

## Technologies

The project uses:

- Python
- Flask
- Pytest
- Coverage.py
- Locust
- JSON
- Git / GitHub

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/Kiyat1724/Python_Testing.git
cd Python_Testing
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows PowerShell

Activate the virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, temporarily allow it for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Set Flask to use `server.py`.

### Windows PowerShell

```powershell
$env:FLASK_APP="server.py"
flask run
```

The application is then available at:

```text
http://127.0.0.1:5000/
```

## Data Persistence

The application uses JSON files instead of a database.

The main data files are:

- `clubs.json`: stores club information and current points balances;
- `competitions.json`: stores competitions and their remaining available places;
- `bookings.json`: stores bookings made by clubs.

Bookings are persisted so that booking history is not lost when the Flask server is restarted.

This persistence is also used to enforce the maximum number of places that a club can book for the same competition.

## Booking Business Rules

The booking business logic has been separated from the Flask route into a dedicated `purchase_places()` function.

This separation makes the business rules easier to understand, maintain, and test independently from the HTTP layer.

A booking is accepted only when all business rules are satisfied.

The application verifies that:

- the requested number of places is greater than `0`;
- the club has enough points;
- the competition has enough available places;
- the club does not book more than 12 places in total for the same competition;
- the competition has not already taken place.

For a successful booking:

- the club's points balance is reduced;
- the competition's available places are reduced;
- the booking is stored in `bookings.json`;
- the updated club and competition data are persisted in their respective JSON files.

## Dynamic Booking Limit

The booking form dynamically calculates the maximum number of places that can be requested.

The limit takes into account:

- the remaining allowance before reaching the 12-place cumulative limit;
- the number of places still available in the competition;
- the number of points currently available to the club.

The backend performs the same business validations independently of the interface.

This ensures that business rules cannot be bypassed simply by modifying the HTML form.

## Past Competitions

Past competitions cannot be booked.

The application handles this rule at two levels:

1. the booking option is not displayed for past competitions in the interface;
2. the backend booking logic rejects attempts to book a past competition.

This provides both a better user experience and server-side enforcement of the business rule.

## Points Board

The application provides a public points board displaying the clubs and their current points balances.

This allows users to consult the points available to each club without requiring authentication.

# Testing Strategy

Automated tests are implemented with Pytest.

Following the QA review, the test suite was reorganized by test level and application responsibility rather than by GitHub issue number.

The current structure is:

```text
tests/
├── integration/
│   ├── __init__.py
│   ├── test_booking_journey.py
│   └── test_user_journey.py
├── unit/
│   ├── __init__.py
│   ├── test_book.py
│   ├── test_display_points.py
│   ├── test_load.py
│   ├── test_purchase_places.py
│   ├── test_purchase_places_route.py
│   ├── test_save.py
│   └── test_show_summary.py
├── __init__.py
└── conftest.py
```

This organization makes the purpose of each test easier to identify and keeps tests targeting the same function or responsibility together.

## Unit Tests

The majority of the automated test suite consists of focused unit tests.

### Loading functions

`test_load.py` verifies the three JSON loading functions:

- `loadClubs()`;
- `loadCompetitions()`;
- `loadBookings()`.

Temporary files are used during these tests so that the application's real JSON data is not modified.

### Saving functions

`test_save.py` verifies the three JSON persistence functions:

- `saveClubs()`;
- `saveCompetitions()`;
- `saveBookings()`.

These tests verify that application data is correctly written to JSON storage.

### Booking business logic

`test_purchase_places.py` groups the tests associated with the `purchase_places()` business function.

The tests verify:

- successful bookings;
- insufficient club points;
- insufficient competition capacity;
- zero booking quantities;
- negative booking quantities;
- bookings for past competitions;
- the cumulative 12-place booking limit;
- persistence of bookings in `bookings.json`;
- persistence of updated club points and competition places.

Keeping these tests together reflects the responsibility of the `purchase_places()` function and makes the business rules easier to review.

### Flask route behavior

Additional focused tests verify individual Flask routes and their responsibilities:

- `test_show_summary.py`: handling of an unknown email;
- `test_book.py`: rejection of a past competition;
- `test_purchase_places_route.py`: behavior of the `/purchasePlaces` route and its booking validations;
- `test_display_points.py`: public display of the clubs' points board.

## Integration Tests

Integration testing is deliberately limited to complete and coherent user journeys involving several consecutive application actions.

### User journey

`test_user_journey.py` verifies that a user can:

1. log in with a valid club email;
2. access the application;
3. consult the points board;
4. log out successfully.

### Booking journey

`test_booking_journey.py` verifies a complete booking workflow:

1. the club secretary logs in;
2. a future competition is selected;
3. the `/book` route is successfully accessed;
4. places are requested;
5. the booking is processed;
6. the success confirmation is displayed;
7. the club's points are reduced;
8. the competition's available places are reduced;
9. the booking is recorded.

These integration tests verify that routes, templates, business logic, and application data work together correctly across a complete user workflow.

## Running the Tests

Run the complete automated test suite with:

```bash
pytest -v
```

Current result:

```text
24 passed
```

## Test Coverage

Test coverage is measured using Coverage.py.

Run:

```bash
coverage erase
coverage run -m pytest
coverage report -m
```

Current results:

```text
server.py: 100%
TOTAL: 100%
```

The project therefore exceeds the required minimum test coverage of 60%.

An optional local HTML report can be generated with:

```bash
coverage html
```

The generated `.coverage` file and `htmlcov/` directory are ignored by Git because they are generated test artifacts rather than source code.

# Performance Testing

Performance tests are implemented using Locust.

Run the Flask application, then start Locust with:

```bash
locust -f locustfile.py
```

Open the Locust interface at:

```text
http://localhost:8089
```

The performance test scenario is designed for six simultaneous users.

The performance requirements are:

- data retrieval and page loading in less than 5 seconds;
- data updates in less than 2 seconds.

Locust is used to simulate concurrent users and measure application response times under load.

Generated performance reports are not versioned as source code.

# Git and QA Workflow

Git branches are used to isolate bug fixes, features, and application improvements.

Dedicated branches were created during development to keep changes traceable and to avoid introducing unfinished work directly into the main branch.

Individual bug and feature branches were used during the debugging phase, while the final validated corrections were consolidated through:

```text
improvement/final-corrections
```

Once the complete automated test suite was successful, the validated version was integrated into `master`.

The `master` branch is therefore the project's source of truth and contains the stable, functional version of the application.

A dedicated QA branch was then created from the final `master` branch:

```text
qa/final-review
```

At the start of the final QA review, `master` and `qa/final-review` point to the same validated application state.

The QA branch is used for final code review and quality assurance and is not intended to be merged back into `master`.

The final QA review covers:

- business-rule validation;
- Flask routes and templates;
- JSON persistence;
- unit and integration tests;
- test coverage;
- performance testing;
- project documentation.

This workflow keeps the stable application identifiable in `master` while maintaining a dedicated branch for final quality review.

# Key Quality Improvements

The main improvements implemented during this project include:

- safer handling of unknown email addresses;
- prevention of bookings for past competitions;
- prevention of zero and negative bookings;
- validation of available club points;
- validation of competition capacity;
- enforcement of the cumulative 12-place booking limit;
- persistent booking history with `bookings.json`;
- dynamic booking limits based on points, capacity, and previous bookings;
- server-side enforcement of business rules;
- persistence of club points and competition places;
- public points board display;
- separation of booking business logic from the Flask route;
- focused unit testing of business rules and application functions;
- complete integration tests based on coherent user journeys;
- JSON loading and persistence testing;
- automated test coverage measurement;
- performance testing with Locust;
- structured quality-assurance workflow with Git.

# Professional Perspective

This project was completed as part of my Python development training and contributes to my broader career transition toward functional cybersecurity consulting.

Although GUDLFT Registration is not a cybersecurity application, the project strengthened several skills that are directly transferable to functional consulting, software quality, and cybersecurity-oriented environments:

- understanding functional requirements and translating them into verifiable business rules;
- identifying defects and analyzing their impact on application behavior;
- comparing expected and actual behavior;
- designing test scenarios from functional requirements;
- distinguishing user-interface controls from backend validation;
- validating data consistency and persistence;
- considering how application rules can be bypassed if they are enforced only on the client side;
- documenting technical and functional decisions;
- using Git branches to improve traceability and quality assurance;
- using automated tests, coverage measurement, and performance testing as evidence that requirements are respected;
- communicating between functional requirements and technical implementation.

These practices are particularly relevant to my objective of working as a functional cybersecurity consultant, where requirements analysis, control validation, risk awareness, traceability, testing, documentation, and communication between technical and business stakeholders are essential.

## Repository

GitHub repository:

`https://github.com/Kiyat1724/Python_Testing`