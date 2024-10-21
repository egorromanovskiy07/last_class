import pytest
import requests

from api.entities import Booking
from api.client import Client


def check_response_id(response: requests.Response, booking_id: str):
    booking_ids = []
    for booking in response.json():
        booking_ids.append(booking['bookingid'])
    assert booking_id in booking_ids, f'booking_id = {booking_id} is not in booking_ids = {booking_ids}'


class TestCreateBooking:
    @pytest.fixture(scope='class')
    def json_booking(self, client: Client, booking: dict):
        collected = client.get_booking(booking['bookingid'])
        assert collected.status_code == 200
        return collected.json()

    def test_first_name(self, json_booking: dict, booking_data: Booking):
        assert json_booking['firstname'] == booking_data.first_name

    def test_last_name(self, json_booking: dict, booking_data: Booking):
        assert json_booking['lastname'] == booking_data.last_name

    def test_total_price(self, json_booking: dict, booking_data: Booking):
        assert json_booking['totalprice'] == booking_data.total_price

    def test_deposit_paid(self, json_booking: dict, booking_data: Booking):
        assert json_booking['depositpaid'] == booking_data.deposit_paid

    def test_check_in(self, json_booking: dict, booking_data: Booking):
        assert json_booking['bookingdates']['checkin'] == booking_data.date_in

    def test_check_out(self, json_booking: dict, booking_data: Booking):
        assert json_booking['bookingdates']['checkout'] == booking_data.date_out

    def test_additional_needs(self, json_booking: dict, booking_data: Booking):
        assert json_booking['additionalneeds'] == booking_data.additional_needs


def test_get_booking_by_id(client, booking):
    booking_response = client.get_booking(booking['bookingid'])
    assert booking_response.status_code == 200
    json_data = booking_response.json()
    assert json_data['firstname'] == booking['booking']['firstname']
    assert json_data['lastname'] == booking['booking']['lastname']
    assert json_data['totalprice'] == booking['booking']['totalprice']
    assert json_data['depositpaid'] == booking['booking']['depositpaid']
    assert json_data['bookingdates']['checkin'] == booking['booking']['bookingdates']['checkin']
    assert json_data['bookingdates']['checkout'] == booking['booking']['bookingdates']['checkout']
    assert json_data['additionalneeds'] == booking['booking']['additionalneeds']


def test_get_booking_id_by_firstname(client, booking: dict, booking_data: Booking):
    response = client.get_booking(params={'firstname': booking_data.first_name})
    assert response.status_code == 200
    check_response_id(response, booking['bookingid'])


def test_get_booking_id_by_lastname(client, booking: dict, booking_data: Booking):
    response = client.get_booking(params={'lastname': booking_data.last_name})
    assert response.status_code == 200
    check_response_id(response, booking['bookingid'])


@pytest.mark.skip(reason='PROJECT-001, Known issue')
def test_get_booking_id_by_checkin(client, booking):
    response = client.get_booking(params={'checkin': booking['booking']['bookingdates']['checkin']})
    assert response.status_code == 200
    check_response_id(response, booking['bookingid'])


@pytest.mark.skip(reason='PROJECT-002, Known issue')
def test_get_booking_id_by_checkout(client, booking):
    response = client.get_booking(params={'checkout': booking['booking']['bookingdates']['checkout']})
    assert response.status_code == 200
    check_response_id(response, booking['bookingid'])


@pytest.mark.skip(reason='PROJECT-003, Known issue')
def test_get_booking_id_by_multiple_params(client, booking):
    response = client.get_booking(params={
        'firstname': booking['booking']['firstname'],
        'lastname': booking['booking']['lastname'],
        'checkin': booking['booking']['bookingdates']['checkin'],
        'checkout': booking['booking']['bookingdates']['checkout']
    })
    assert response.status_code == 200
    check_response_id(response, booking['bookingid'])


def test_delete_booking(client, booking):
    response = client.delete_booking(booking['bookingid'])
    assert response.status_code == 201
    booking_response = client.get_booking(booking['bookingid'])
    assert booking_response.status_code == 404


def test_update_booking(client, booking_to_write):
    response = client.update_booking(booking_to_write['bookingid'])
    assert response.status_code == 200
    response_data = response.json()
    updated_booking = client.get_booking(booking_to_write['bookingid'])
    assert updated_booking.status_code == 200
    updated_booking_data = updated_booking.json()
    assert updated_booking_data['firstname'] == response_data['firstname']
    assert updated_booking_data['lastname'] == response_data['lastname']
    assert updated_booking_data['totalprice'] == response_data['totalprice']
    assert updated_booking_data['depositpaid'] == response_data['depositpaid']
    assert updated_booking_data['bookingdates']['checkin'] == response_data['bookingdates']['checkin']
    assert updated_booking_data['bookingdates']['checkout'] == response_data['bookingdates']['checkout']
    assert updated_booking_data['additionalneeds'] == response_data['additionalneeds']
