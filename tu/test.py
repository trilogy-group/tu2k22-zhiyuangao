import requests
# 1. post to sign up a user

r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": "string", "password": "string"})
print(r)
print(r.json())
