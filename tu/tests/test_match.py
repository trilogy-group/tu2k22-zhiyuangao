import pytest import requests 
url = "http://localhost:8080/"


def prepare():
    # 1. Sign up
    name = "Foooo.Boo_yes"
    email = name+"@example.com"
    r = requests.post(url+'api/v1/auth/signup/', {"email": name+"@email.com", "password": "string", "name":name})
    token = r.json()['token']

    # 2. Create sector
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    name = "sector1"
    description = "description1"
    r = requests.post(url+'api/v1/sectors/', {'name':name, 'description':description}, headers=header)

    # 3. Create stock
    name = "stock1"
    r = requests.post(url+'api/v1/stocks/', { "name": name, "price": "100.00", "sector": 0, "unallocated": 0, "total_volume": 0}, headers=headers)


def test_successful_match() :
    # Create Sell Order Price > Market Price
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "SELL", "bid_price": 120, "bid_volume": 5}, headers=headers)
    # Create Buy Order Price > Sell Order
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "BUY", "bid_price": 180, "bid_volume": 5}, headers=headers)

    # Match orders
    # The transaction price is determined by the late-comer -- 180
    path = "api/v1/match/"
    r = requests.post(url=url+path)
    assert(str(r) == "<Response [200]>")


def test_fillfulled_buy():
    # Create Sell Order Price > Market Price
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "SELL", "bid_price": 200, "bid_volume": 5}, headers=headers)
    # Create Buy Order Price > Market Price, while Buy Price < Sell Price
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "BUY", "bid_price": 190, "bid_volume": 5}, headers=headers)

    # Match orders
    # The transaction price is determined by the late-comer -- 190
    path = "api/v1/match/"
    r = requests.post(url=url+path)
    assert(str(r) == "<Response [200]>")


def test_fillfulled_sell():
    # Create Sell Order Price > Market Price
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "SELL", "bid_price": 20, "bid_volume": 5}, headers=headers)
    # Create Buy Order Price > Market Price, while Buy Price < Sell Price
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "BUY", "bid_price": 190, "bid_volume": 5}, headers=headers)

    # Match orders
    # The transaction price is determined by the fillfulled price -- 20
    path = "api/v1/match/"
    r = requests.post(url=url+path)
    assert(str(r) == "<Response [200]>")

    # Because the sell was fillfulled by the market, the market sells to the buy order
    # Finally, there are no incomplete orders, list orders to double check
    path = "api/v1/match/"
    r = requests.get(url=url+path)
    assert(str(r) == "<Response [200]>")


def test_order_sort():
    # Create Sell Order 1 Price = 300
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "SELL", "bid_price": 300, "bid_volume": 5}, headers=headers)
    # Create Sell Order 2 Price = 400
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "SELL", "bid_price": 400, "bid_volume": 5}, headers=headers)

    # Create Buy Order 1 = 350
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "BUY", "bid_price": 350, "bid_volume": 5}, headers=headers)
    # Create Buy Order 2 = 480
    r = requests.post(url+'/api/v1/orders', { "stock_id": 1, 'type': "BUY", "bid_price": 480, "bid_volume": 5}, headers=headers)

    # Match orders
    # Buy Order 2 will complete Sell Order 1 (lowest bid)
    # Market Price set to 480
    path = "api/v1/match/"
    r = requests.post(url=url+path)
    assert(str(r) == "<Response [200]>")

    # Buy Order 1 will complete Sell Order 2
    # Market Price set to 350

    # Finally, there are no incomplete orders, list orders to double check
    path = "api/v1/match/"
    r = requests.get(url=url+path)
    assert(str(r) == "<Response [200]>")


