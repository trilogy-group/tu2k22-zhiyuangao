import pytest import requests
url = "http://localhost:8080/"


def test_signup():
    name = "Foooo.Boo_yes"
    email = name+"@example.com"
    r = requests.post(url+'api/v1/auth/signup', {"email": name+"@email.com", "password": "string", "name":name})
    assert (str(r) == "<Response [201]>")
    assert (str(r.json()) == "{\"id\": 0}")


def profile(token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post(url+'api/v1/users/profile', headers=headers)
    print(r)
    print(r.json())
    print('user profile emitted!')


def logout(token):
   # test log out
   headers = {
        "Content-Type": "application/json",
        "Authorization": token
   }
   r = requests.post(url+'api/v1/auth/logout', headers=headers)
   print(r)
   print('Logged out!')
