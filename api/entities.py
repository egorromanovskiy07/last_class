from dataclasses import dataclass

from api.helpers import generate_string


@dataclass
class CheckDate:
    in_: str
    out: str


@dataclass
class Name:
    first: str
    last: str


class Booking:
    def __init__(self, name: Name, total_price: int, date: CheckDate, additional_needs: str, deposit_paid=False):
        self.first_name = name.first
        self.last_name = name.last
        self.total_price = total_price
        self.date_in = date.in_
        self.date_out = date.out
        self.additional_needs = additional_needs
        self.deposit_paid = deposit_paid

    @classmethod
    def from_raw_data(cls, check_in: str, check_out: str, total_price: int, additional_needs: str, deposit_paid: bool):
        name = Name(first=generate_string(7), last=generate_string(7))
        check_date = CheckDate(in_=check_in, out=check_out)
        return cls(name, total_price, check_date, additional_needs, deposit_paid)

    def create_payload(self):
        payload = {
            'firstname': self.first_name,
            'lastname': self.last_name,
            'totalprice': self.total_price,
            'depositpaid': self.deposit_paid,
            'bookingdates': {
                'checkin': self.date_in,
                'checkout': self.date_out
            },
            'additionalneeds': self.additional_needs
        }
        return payload
