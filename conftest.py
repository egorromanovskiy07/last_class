import pytest

from api.entities import Booking
from api.client import Client


def create_booking(client: Client, booking_data_: Booking) -> dict:
    payload = booking_data_.create_payload()
    response = client.create_booking(payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope='session')
def booking_data():
    data_ = Booking.from_raw_data(check_in='2024-10-01', check_out='2024-10-01', total_price=100,
                                  additional_needs='Breakfast', deposit_paid=False)
    return data_


@pytest.fixture(scope='session')
def booking(client: Client, booking_data: Booking) -> dict:
    json_data = create_booking(client, booking_data)
    booking_id = json_data['bookingid']
    yield json_data
    client.delete_booking(booking_id)


@pytest.fixture(scope='function')
def booking_to_write(client: Client, booking_data: Booking):
    json_data = create_booking(client, booking_data)
    booking_id = json_data['bookingid']
    yield json_data
    client.delete_booking(booking_id)


@pytest.fixture(scope='session')
def client():
    client = Client()
    return client
