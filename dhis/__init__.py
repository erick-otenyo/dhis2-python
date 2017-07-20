import requests

BASE_URL = 'https://play.dhis2.org/release1/api/'

AUTH = ('admin','district')

class AuthMIssingError(Exception):
    pass


if AUTH is None:
    raise AuthMIssingError(
        "All methods require an username and password"
    )

session = requests.Session()
session.auth = AUTH