import requests, subprocess
import time

#url = "https://8080-trilogygrou-tu2k22zhiyu-sq8b22pxndn.ws.legacy.devspaces.com/"
url = "http://localhost:8080/"

def signup(name='user1'):
    email = name+"@example.com"
    # 1. post to sign up a user
    #r = requests.post('http://127.0.0.1:8080/api/v1/auth/signup', {"email": name+"@email.com", "password": "string", "name":name})
    r = requests.post(url+'api/v1/auth/signup/', {"email": name+"@email.com", "password": "password", "name":name})
    print(r)
    print(r.json())
    print('user '+name+' signed up')


def login(name='user1'):
    # log in
    r = requests.post(url+'api/v1/auth/login/', {"password": "password", "email":name+"@email.com"})
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


def postSector(token):
    # create a new sector
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post(url+'api/v1/sectors/', {'name':'sector1', 'description':'description2'}, headers=headers)
    print(r)
    print(r.json())


def patchSector(token):
    # patch a sector
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.patch('http://127.0.0.1:8080/api/v1/sectors/1', {'name':'sectorname2', 'description':'description2'}, headers=headers)
    print(r)
    print(r.json())


def listStocks():
    # list all stocks
    r = requests.get('http://127.0.0.1:8080/api/v1/stocks')
    print(r)
    print(r.json())
    print('Listed stocks!')


def createStocks(token):
    # create stocks
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post('http://127.0.0.1:8080/api/v1/stocks/', {  "name": "string", "price": "1.00", "sector": 0, "unallocated":100000, "total_volume": 100000}, headers=headers)
    print(r)
    print(r.json())
    print('Created stocks')


# Get a stock by id
#r = requests.get('http://127.0.0.1:8080/api/v1/stocks/1')

# List all Orders
def listOrders(token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.get('http://127.0.0.1:8080/api/v1/orders', headers=headers)
    print(r)
    print(r.json())
    print('Listed orders')


def createOrders(token, type_s):
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    r = requests.post('http://127.0.0.1:8080/api/v1/orders/', { "stock_id": 0, 'type': type_s, "bid_price": 1, "bid_volume": 1}, headers=headers)
    print(r)
    print(r.json())


def signupcase3():
    name = 'A'
    email = "BB@A.com"
    # 1. post to sign up a user
    r = requests.post(url+'api/v1/auth/signup/', {"email": email, "name":name, "password": "pass@123"})
    print(r)
    print(r.json())
    print('user '+name+' signed up')


def signupbuyer(name):
    cmd = "curl --location --request POST 'http://127.0.0.1:8080/api/v1/auth/signup/' --header 'Content-Type: application/json' --data-raw '{\"password\": \"admin\", \"email\": \""+name+"@trilogy.com\", \"name\": \""+name+"\"}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    print(p.communicate())

def loginbuyer(name):
    cmd = "curl --location --request POST 'http://127.0.0.1:8080/api/v1/auth/login/' --header 'Content-Type: application/json' --data-raw '{\"password\": \"admin\", \"email\": \""+name+"@trilogy.com\", \"name\": \""+name+"\"}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    s = p.communicate()
    print(s)
    return str(s).split(',')[0].split(':')[1].strip('}\"\'')

def createSectorCurl(token):
    cmd = "curl --location --request POST 'http://127.0.0.1:8080/api/v1/sectors/' --header 'Authorization: Token "+token+"' --header 'Content-Type: application/json' --data-raw '{\"name\": \"Technology1\", \"description\": \"Stonks1\"}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    print(p.communicate())

def createStocksCurl(token):
    cmd = "curl --location --request POST 'http://127.0.0.1:8080/api/v1/stocks/' --header 'Authorization: Token "+token+"' --header 'Content-Type: application/json' --data-raw '{\"name\": \"TCSNEW\", \"price\": 1.00, \"sector\": 0, \"unallocated\": 10000000,\"total_volume\": 50000}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    print(p.communicate())

def createOrderCurl(token, type_s):
    cmd = "curl --location --request POST 'http://127.0.0.1:8080/api/v1/orders/' --header 'Authorization: Token "+token+"' --header 'Content-Type: application/json' --data-raw '{\"type\": \""+type_s+"\", \"stock\": \"0\", \"bid_price\": \"1.00\", \"bid_volume\": 1}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    print(p.communicate())

if __name__ == '__main__':
    #signupbuyer('seller')

    buyer = loginbuyer('buyer')
    print(buyer)

    createSectorCurl(buyer)
    createStocksCurl(buyer)

    loop = 50000
    for i in range(loop):
        createOrderCurl(buyer, 'BUY')
    """
    #signup('user1')
    signup('user2')

    #token1 = login('user1')
    token2 = login('user2')
    #profile(token1)
    #profile(token1)
    profile(token2)
    
    #logout(token1)
    
    #listSectors()
    #listSectors()

    #postSector(token2)
    #createStocks(token2)
    listOrders(token2)
    createOrders(token2)
    listOrders(token2)

    logout(token2)
    """


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


"""
