import pytest
from app.models import Reservation, Seat, Schedule, User


def test_create_reservation_success(setup_database, client):
    response = client.post("/reservations/", json={"seat_id": 1, "schedule_id": 1})
    assert response.status_code == 200
    assert response.json() == None

    db = setup_database
    reservation = db.query(Reservation).filter(Reservation.seat_id == 1, Reservation.schedule_id == 1).first()
    assert reservation is not None


def test_create_reservation_already_reserved(setup_database, client):
    client.post("/reservations/", json={"seat_id": 1, "schedule_id": 1})

    response = client.post("/reservations/", json={"seat_id": 1, "schedule_id": 1})
    assert response.status_code == 400
    assert response.json() == {"detail": "This seat is already reserved for the selected schedule"}


def test_create_reservation_invalid_seat(setup_database, client):
    response = client.post("/reservations/", json={"seat_id": 999, "schedule_id": 1})
    assert response.status_code == 404
    assert "OOPS!" in response.text


def test_create_reservation_invalid_schedule(setup_database, client):
    response = client.post("/reservations/", json={"seat_id": 1, "schedule_id": 999})
    assert response.status_code == 404
    assert "OOPS!" in response.text


def test_delete_reservation_success(setup_database, client):
    client.post("/reservations/", json={"seat_id": 2, "schedule_id": 1})

    response = client.delete("/reservations/1")
    assert response.status_code == 200

    db = setup_database
    reservation = db.query(Reservation).filter(Reservation.id == 1).first()
    assert reservation is None


def test_delete_reservation_not_found(client):
    response = client.delete("/reservations/999")
    assert response.status_code == 404
    assert "OOPS!" in response.text
