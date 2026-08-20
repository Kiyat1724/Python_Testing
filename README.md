# GUDLFT Registration

## Project Overview

GUDLFT Registration is a lightweight Flask proof-of-concept application for managing competition bookings between sports clubs.

The objective of this project is to improve an existing Python web application by identifying bugs, implementing business rules, improving data persistence, and building an automated testing strategy.

The project focuses particularly on software quality, debugging, testing, validation of business requirements, and performance testing.


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

If PowerShell prevents script execution, you can temporarily allow it for the current session:

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

The booking logic has been separated from the Flask route into a dedicated `purchase_places()` function.

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
- the updated club and competition data are persisted in their JSON files.


## Dynamic Booking Limit

The booking form dynamically calculates the maximum number of places that can be requested.

The limit takes into account:

- the remaining allowance before reaching the 12-place limit;
- the number of places still available in the competition;
- the number of points currently available to the club.

The backend performs the same business validations independently of the interface.

This ensures that application rules cannot be bypassed simply by modifying the HTML form.


## Past Competitions

Past competitions cannot be booked.

The application handles this rule at two levels:

1. the booking option is not displayed for past competitions in the interface;
2. the backend booking logic also rejects an attempt to book a past competition.

This provides both a better user experience and server-side validation of the business rule.


## Points Board

Club secretaries can access a points board displaying the clubs and their current points balances.

This provides visibility of the points available to the different clubs.


# Testing Strategy

Automated tests are implemented with Pytest.

The test suite is organized by test type and functionality rather than by GitHub issue number.

```text
tests/
├── integration/
├── unit/
├── functional/
└── conftest.py
```

This organization makes the test suite easier to understand and maintain.


## Unit Tests

Unit tests focus primarily on the `purchase_places()` business logic.

They verify cases including:

- successful booking;
- insufficient club points;
- insufficient competition capacity;
- zero or negative booking quantities;
- booking a past competition;
- exceeding the maximum number of places allowed.

These tests validate the booking rules independently from the Flask interface.


## Integration Tests

Integration tests verify interactions between the Flask application, routes, business logic, templates, and persisted data.

They cover scenarios including:

- unknown email authentication;
- booking limits;
- insufficient points;
- competition capacity;
- past competitions;
- points updates;
- points display;
- JSON persistence;
- booking persistence in `bookings.json`.


## JSON Persistence Tests

Persistence tests verify that a successful booking correctly updates the application's JSON data.

The tests verify both:

- the updated club points;
- the updated number of competition places.

Booking persistence in `bookings.json` is also tested.


## Running the Tests

Run the complete automated test suite with:

```bash
pytest -v
```

Current test result:

```text
17 passed
```


## Test Coverage

Test coverage is measured using Coverage.py.

Run:

```bash
coverage run -m pytest
coverage report -m
```

Current results:

```text
TOTAL coverage: 96%
server.py coverage: 86%
```

The project therefore exceeds the required minimum coverage of 60%.


# Performance Testing

Performance tests are implemented using Locust.

Run Locust with:

```bash
locust -f locustfile.py
```

Then open:

```text
http://localhost:8089
```

The performance test scenario is designed for 6 simultaneous users.

The expected performance requirements are:

- data retrieval and page loading in less than 5 seconds;
- data updates in less than 2 seconds.

Locust is used to simulate concurrent users and measure the application's response times under load.


# Git and QA Workflow

The project uses Git branches to isolate bug fixes and application improvements.

Dedicated branches were used during development for individual issues and features.

A dedicated QA branch is used for the final review:

```text
qa/final-review
```

The QA branch contains the corrected application, automated tests, persistence improvements, performance tests, and final quality validation.

This workflow helps separate development work from quality-assurance validation and provides traceability of the changes made during the project.


# Key Quality Improvements

The main improvements implemented during this project include:

- safer handling of unknown email addresses;
- prevention of bookings for past competitions;
- prevention of zero and negative bookings;
- validation of available club points;
- validation of competition capacity;
- enforcement of the 12-place cumulative booking limit;
- dynamic booking limits in the user interface;
- server-side validation of business rules;
- persistence of club, competition, and booking data;
- points board display;
- separation of business logic from Flask routes;
- unit and integration testing;
- JSON persistence testing;
- test coverage measurement;
- performance testing with Locust;
- structured QA workflow with Git.


# Professional Perspective

This project was completed as part of my Python development training and contributes to my broader career transition toward functional IT and cybersecurity consulting.

Beyond Python development itself, the project allowed me to strengthen skills that are also relevant to functional consulting and software quality:

- understanding and translating functional requirements into business rules;
- identifying application defects and analyzing their impact;
- validating expected versus actual application behavior;
- designing test scenarios from business requirements;
- separating user-interface controls from backend validation;
- improving data consistency and persistence;
- documenting technical and functional decisions;
- using Git branches to support traceability and quality assurance;
- using automated testing and performance testing to provide evidence that requirements are respected.

These practices are transferable to functional cybersecurity and GRC-oriented environments, where requirements analysis, control validation, risk awareness, traceability, testing, and communication between technical and business stakeholders are important.


## Repository

GitHub repository:

`https://github.com/Kiyat1724/Python_Testing`
