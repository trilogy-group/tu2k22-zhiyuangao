import requests

# 1. post to sign up a user
r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string@email.com", "password": "string", "name":"zhiyuan"})
print(r)
print(r.json())

# dup username
r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string@email.com", "password": "string", "name":"zhiyuan"})
assert(str(r) == '<Response [401]>')
assert(r.json() == 'User sign-up failed')
print("TEST passed: duplicated username")

# dup password
r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string@email.com", "password": "string", "name":"zhiyuan"})
print(r)
print(r.json())

# log in
r = requests.post('http://127.0.0.1:8080/api/v1/auth/login', {"password": "string", "username":"zhiyuan"})
print(r)
print(r.json())

# wrong password
r = requests.post('http://127.0.0.1:8080/api/v1/auth/login', {"password": "string wrong", "username":"zhiyuan"})
print(r)
print(r.json())

# wrong username
r = requests.post('http://127.0.0.1:8080/api/v1/auth/login', {"password": "string", "username":"wrong zhiyuan"})
print(r)
print(r.json())

# test log out
r = requests.post('http://127.0.0.1:8080/api/v1/auth/logout', {"token": "123"})
print(r)
print(r.json())

# user profile
r = requests.post('http://127.0.0.1:8080/api/v1/users/profile', {"token": "123"})
print(r)
print(r.json())

# token AIM9vfBai-tSnozCXoL5GiLkMuu2KtPTDIeYUSwkHtk
r = requests.post('http://127.0.0.1:8080/api/v1/users/profile', {"token": "AIM9vfBai-tSnozCXoL5GiLkMuu2KtPTDIeYUSwkHtk"})
print(r)
print(r.json())


# get sectors
r = requests.get('http://127.0.0.1:8080/api/v1/sectors')
print(r)
print(r.json())

# post sectors
r = requests.post('http://127.0.0.1:8080/api/v1/sectors', {'name':'sectorname2', 'description':'description2'})
print(r)
print(r.json())


