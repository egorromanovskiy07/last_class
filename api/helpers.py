import random
import string


def generate_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))




