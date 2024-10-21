import requests

from api.entities import Booking

BASE_URL = 'https://restful-booker.herokuapp.com/booking'


class Client:
    def __init__(self):
        self.endpoint = ''
        self._auth_header = self.create_auth_header()
        self.url = BASE_URL

    @staticmethod
    def create_auth_header() -> dict:
        auth_url = 'https://restful-booker.herokuapp.com/auth'
        body = {
            "username": "admin",
            "password": "password123"
        }
        token = requests.post(auth_url, json=body).json()
        cookie_value = f'token={token["token"]}'
        auth_header = {'Cookie': cookie_value}
        return auth_header

    def create_booking(self, payload: dict) -> requests.Response:
        return requests.post(self.url + self.endpoint, json=payload)

    def delete_booking(self, booking_id: str) -> requests.Response:
        url = self.url + f'/{booking_id}'
        return requests.delete(url, headers=self._auth_header)

    def get_booking(self, booking_id='', **kwargs) -> requests.Response:
        url = self.url
        if booking_id:
            url += f'/{booking_id}'
        return requests.get(url, **kwargs)

    def update_booking(self, booking_id: str) -> requests.Response:
        """
        :param booking_id:
        :return:
        """
        data = Booking.from_raw_data(
            total_price=80,
            deposit_paid=False,
            check_in='2024-12-01',
            check_out='2025-01-07',
            additional_needs='No breakfast'
        )
        payload = data.create_payload()
        return requests.put(self.url + f'/{booking_id}', headers=self._auth_header, json=payload)
