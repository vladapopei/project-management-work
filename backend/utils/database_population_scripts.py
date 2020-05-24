import requests
from requests.auth import HTTPBasicAuth
from helpr.database import BusinessSchema

ROOT_DOMAIN = "http://localhost:5000/"


def add_user(username, password):
    """"
    Sends a post request to /accounts/users which will create a new user with the provided username and password.
    """
    json = dict(username=username, password=password)
    return requests.post(ROOT_DOMAIN + 'account/users', json=json)


def add_business(business: dict, username: str, password: str):
    r = requests.post(ROOT_DOMAIN + 'business/register',
                      json=business,
                      auth=HTTPBasicAuth(username, password))
    return r


def add_posting(posting: dict, username: str, password: str):
    r = requests.post(ROOT_DOMAIN + 'business/posting',
                      json=posting,
                      auth=HTTPBasicAuth(username, password))
    return r


if __name__ == '__main__':
    add_user('test_user_1', 'password')
    add_user('test_user_2', 'password')
    add_user('test_user_3', 'password')
    add_user('test_user_4', 'password')
    b = add_business(dict(name='charlies big business',
                          contact_email='get tae fuck',
                          contact_number='not a chance'),
                     username='test_user_1',
                     password='password')
    p = add_posting(dict(title="lets do this", pricing=5.55),
                     username='test_user_1',
                     password='password')
    print(p)
