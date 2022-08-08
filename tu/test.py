import requests
import time

url = "https://8080-trilogygrou-tu2k22zhiyu-sq8b22pxndn.ws.legacy.devspaces.com/"

def signup(name='user1'):
    email = name+"@example.com"
    # 1. post to sign up a user
    #r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": name+"@email.com", "password": "string", "name":name})
    r = requests.post(url+'api/v1/auth/signup', {"email": name+"@email.com", "password": "string", "name":name})
    print(r)
    print(r.json())
    print('user '+name+' signed up')


def login(name='user1'):
    # log in
    r = requests.post(url+'api/v1/auth/login', {"password": "string", "username":name})
    print(r)
    print(r.json())
    return r.json()['token']


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


def listSectors():
    # get sectors
    r = requests.get(url+'api/v1/sectors')
    print(r)
    print(r.json())
    print('listed sectors!')


if __name__ == '__main__':
    signup('user1')
    signup('user2')

    token1 = login('user1')
    token2 = login('user2')
    profile(token1)
    profile(token1)
    profile(token2)
    
    logout(token1)
    logout(token2)
    
    listSectors()
    listSectors()




# dup username
"""
r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string@email.com", "password": "string", "name":"user1"})
assert(str(r) == '<Response [401]>')
assert(r.json() == 'User sign-up failed')
print("TEST passed: duplicated username")
"""

# dup password
"""
r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string@email.com", "password": "string", "name":"zhiyuan"})
print(r)
print(r.json())
"""

"""
# wrong password
r = requests.post('http://127.0.0.1:8080/api/v1/auth/login', {"password": "string wrong", "username":"zhiyuan"})
print(r)
print(r.json())

# wrong username
r = requests.post('http://127.0.0.1:8080/api/v1/auth/login', {"password": "string", "username":"wrong zhiyuan"})
print(r)
print(r.json())


# post sectors
r = requests.post('http://127.0.0.1:8080/api/v1/sectors', {'name':'sectorname2', 'description':'description2'})
print(r)
print(r.json())

# patch a sector
r = requests.patch('http://127.0.0.1:8080/api/v1/sectors/1', {'name':'sectorname2', 'description':'description2'})
print(r)
print(r.json())

# list all stocks
r = requests.get('http://127.0.0.1:8080/api/v1/stocks')
print(r)
print(r.json())

# create all stocks
r = requests.post('http://127.0.0.1:8080/api/v1/stocks', {  "name": "string", "price": "100.00", "sector": 0, "unallocated": 0, "total_volume": 0})
print(r)
print(r.json())


# Get a stock by id
r = requests.get('http://127.0.0.1:8080/api/v1/stocks/1')

# List all Orders
"""
