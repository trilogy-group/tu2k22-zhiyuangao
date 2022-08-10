import requests
import MySQLdb
import secrets
import json, time, logging
from rest_framework import status
from rest_framework.response import Response

db_host = "localhost"
db_user = "sammy"
db_name = "tu"
password = "Ab_19100204"
port = 3306
login_session = {}
connect_pool=[]

class Session:
    def __init__(self, email, token, db_entry_in_users):
        self.useremail = email
        self.data = {'id':db_entry_in_users[0], \
                'name':db_entry_in_users[1], \
                'email':db_entry_in_users[2], \
                'password':db_entry_in_users[3], \
                'availble_funds': int(str(db_entry_in_users[4]).strip('Decimal(\')')), \
                'blocked_funds': int(str(db_entry_in_users[5]).strip('Decimal(\')')) \
            }
        self.token = token
    def __str__(self):
        print(selemailken, self.data)


def connectDB():
    connect=MySQLdb.connect(host=db_host,password=password, user=db_user, db=db_name, port=port)
    print("Connected")
    return connect


def get_connect():
    global connect_pool
    if not connect_pool:
        connect_tmp=connectDB()
        connect_pool.append(connect_tmp)
    return connect_pool.pop()


def register(email, password, name):
    db = get_connect()
    c = db.cursor()
    
    c.execute("SELECT COUNT(*) FROM users;")
    r = c.fetchall()
    if len(r) == 0:
        user_id = 0
    else:
        r = r[0][0]
    user_id = int(r) 
    # TODO: If email identical

    cmd = "INSERT INTO users \n\
            VALUES (" + str(user_id) + \
            ", \"" + name + "\"" +\
            ", \"" + email + "\"" + \
            ", \"" + password + "\"" + \
            ", "+ str(40000) + \
            ", "+ str(0) + ");"
    #print(cmd)
    c.execute(cmd)
    print(c.fetchall())
    db.commit()
    db.close()

    return {"id":user_id}


def login(email, password):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE email =\"" + email +"\"")
    # e.g., ((1, 'zhiyuan', 'string3', 'string', Decimal('40000'), Decimal('0')),)
    r = c.fetchall()[0] # username not found -> raise tuple index error -> exception caught in views
    #print(r)
    if r[3] == password:
        token = secrets.token_urlsafe().strip('=')
        session = Session(email, token, r)
        login_session[token] = session

        db.close()
        return (True, {"token": token})
    else:
        db.close()
        return (False, {"token": "wrong"})


def logout(token):
    try:
        logging.debug('going to del the login session')
        del login_session[token]
    except:
        logging.debug('token deletion failed')
        return Response('No logged in session', status=status.HTTP_401_UNAUTHORIZED)
    return Response('Logout ok.', status=status.HTTP_204_NO_CONTENT)


def profile(token):
    print(login_session, token)
    # authenticate
    data = login_session[token].data
    print(data)
    for k in data:
        data[k] = str(data[k])
    return data


def sectorsGet():
    #try: 
    #    login_session[token]
    #except Exception as e:
    #    print(e)
    #    return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM sectors;")
    data = c.fetchall()
    logging.debug(data)
    if len(data) == 0:
        db.close()
        return Response({}, status=status.HTTP_200_OK)
    result = []
    logging.debug(data)
    for r in data:
        id = r[0]
        name = r[1]
        description = r[2]
        result.append({'id':id, 'name':name, 'description':description})
    logging.debug(result)
    db.close()
    return Response(result, \
            status=status.HTTP_200_OK)


def sectorsGetById(id):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM sectors WHERE id="+str(id)+";")
    r = c.fetchall()
    logging.debug(r)
    if len(r) == 0:
        db.close()
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    id = r[0][0]
    name = r[0][1]
    description = r[0][2]
    db.close()
    return Response({'id':id, 'name':name, 'description':description}, \
            status=status.HTTP_200_OK)


def sectorsPost(name, description, token):
    try: 
        login_session[token]
    except Exception as e:
        print(e)
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    db = get_connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM sectors;")
    r = c.fetchall()
    sector_id = int(r[0][0])

    cmd = "INSERT INTO sectors \n\
            VALUES (" + str(sector_id) + \
            ", \"" + name + "\"" +\
            ", \"" + description + "\");"
    #print(cmd)
    c.execute(cmd)
    #print(c.fetchall())
    db.commit() 
    db.close()

    return Response({'id': sector_id, 'name': name, 'description':description}, status=status.HTTP_201_CREATED)


def sectorsUpdate(id, name, description, token):
    try: 
        login_session[token]
    except Exception as e:
        print(e)
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    db = get_connect()
    c = db.cursor()

    logging.debug('plan to update name:'+str(name)+', description:'+str(description))
    c.execute("SELECT * FROM sectors WHERE id = "+str(id)+";")
    r = c.fetchall()
    print("select result", r)
    if len(r) == 0:
        return Response({'message':"No sector with id "+str(id)}, status.HTTP_406_NOT_ACCEPTABLE)
    
    if description != None and name != None:
        cmd = "UPDATE sectors set description = \"" + \
            description+"\" WHERE id = "+str(id) + \
            " and name = \"" + name + "\";"
    elif name != None:
        cmd = "UPDATE sectors set name = \"" + \
            name + "\" WHERE id = "+str(id) + ';'
    elif description != None:
        cmd = "UPDATE sectors set description = \"" + \
            description+"\" WHERE id = "+str(id) + ';'
    c.execute(cmd)
    print(c.fetchall())
    db.commit() 
    c.execute("SELECT * FROM sectors WHERE id = "+str(id)+";")
    r = c.fetchall()[0]
    name = r[1]
    des = r[2]
    db.close()
    res = {'id':id, 'name':name, 'description':des}
    logging.debug(res)
    return Response(res, status=status.HTTP_200_OK)


def listStocks():
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM stocks;")
    logging.debug('backend: get all stocks')
    res = []
    r = c.fetchall()
    for stock in r:
        #((1, 1, 'stock1', 100, 100, Decimal('200')), (2, 1, 'stock2', 100, 100, Decimal('200')))
        id = int(stock[0])
        sector_id = int(stock[1])
        name = stock[2]
        total_volume = int(stock[3])
        unallocated = int(stock[4])
        price = str(stock[5]).strip("Decimal(\')")
        if '.'not in price:
            price += '.00'
        elif len(price.split('.')[1]) == 1:
            price += '0'

        data = {"id":id, "name":name, "total_volume":total_volume, "sector":sector_id, \
                "unallocated":unallocated, "price":price}
        res.append(data)
        
    #print(r)
    return res


def stocksCreate(name, price, sector_id, unallocated, total_volume, token):
    print('stocksCreate: '+name,  price, sector_id, unallocated, total_volume,)
    print(login_session)
    try: 
        login_session[token]
    except Exception as e:
        print(e)
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT COUNT(*) FROM stocks;")
    r = c.fetchall()[0][0]
    stock_id = int(r)

    cmd = "INSERT INTO stocks \n\
            VALUES (" + str(stock_id) + \
            ", \"" + sector_id + "\"" +\
            ", \"" + name + "\"" + \
            ", \"" + total_volume + "\"" + \
            ", "+ unallocated + \
            ", "+ price + ");"
    #print(cmd)
    c.execute(cmd)
    #print(c.fetchall())
    db.commit()
    db.close()

    return Response({"id": int(stock_id), \
      "name": name, \
      "price": price, "sector": int(sector_id), \
      "unallocated": int(unallocated), \
      "total_volume": int(total_volume) \
      }, status=status.HTTP_201_CREATED)


def getStockById(id, token):
    logging.debug('backen: get stock by id')
    try: 
        login_session[token]
    except Exception as e:
        print(e)
        logging.debug('log in session not found')
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM stocks WHERE id = "+str(id)+';')
    r = c.fetchall()
    logging.debug(r)
    if len(r) == 0:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    data = r[0]
    print(data)
    sector_id = data[1]
    name = data[2]
    total_volume = data[3]
    unallocated = data[4]
    price = str(str(data[5]).strip('Decimal(\')'))
    if '.'not in price:
        price += '.00'
    elif len(price.split('.')[1]) == 1:
        price += '0'

    db.close()

    res = {'id': int(id), 'name': name, 'price': price, 'sector': sector_id, 'unallocated': unallocated, \
            'total_volume': int(total_volume)}
    logging.debug(res)

    return Response(res, status=status.HTTP_200_OK)


def getOrders(token):
    try: 
        login_session[token]
    except Exception as e:
        print(e)
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM orders;")
    r = c.fetchall()

    if len(r) == 0:
        return Response({}, status=status.HTTP_200_OK)

    result = []
    for data in r:
        #print(data)
        id = data[0]
        user_id = data[1]
        stock_id = data[2]
        type_ = data[3]
        create_at = data[4]
        updated_at = data[5]
        order_status = data[6]
        bid_price = data[7]
        bld_volume = data[8]
        executed_volume = data[9]
        result.append({ 'id': id, 'stock': stock_id, 'user': user_id, \
            'type': type_, 'bid_price': bid_price, \
            'bid_volume': bld_volume, \
            'executed_volume': executed_volume, \
            'status': order_status, \
            'created_on': create_at, \
            'updated_on': updated_at })


    print(result)
    return Response(result, status=status.HTTP_200_OK)


def ordersCreate(stock, type, bid_price, bid_volume, token):
    # Authenticate token
    try: 
        user_session = login_session[token]
    except Exception as e:
        print(e)
        return Response('wrong token', status=status.HTTP_401_UNAUTHORIZED)
 
    user_id = user_session.data['id']

    # Check Stock ID availability
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM stocks;")
    r = c.fetchall()
    flag = False
    for db_stock_entry in r:
        if int(db_stock_entry[0]) == int(stock):
            flag = True
            break
    if flag == False:
        return Response('Invalid Stock ID', status=status.HTTP_400_BAD_REQUEST)

    # Check current available funds, block if enough to purchase
    if type == 'BUY':
        c.execute("SELECT available_funds FROM users where id =" + str(user_id)+";")
        r = c.fetchall()
        if len(r) == 0:
            # this shouldn't happen because we already had the token -- aka user added
            return Response('User does not exist', status=status.HTTP_404_NOT_FOUND)
        available_funds = float(r[0][0])
        if available_funds < float(bid_price):
            return Response('Insufficient funds', status=status.HTTP_401_UNAUTHORIZED)
    elif type == 'SELL':
        return Response('TODO', status=status.HTTP_404_NOT_FOUND)
    else:
        return Response('Unknow order type', status=status.HTTP_400_BAD_REQUEST)


    # Find order id
    c.execute("SELECT COUNT(*) FROM orders;")
    r = c.fetchall()
    if len(r) == 0:
        order_id = 0
    else:
        r = r[0][0]
    order_id = int(r)
    
    # Generate response
    #created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    created_at = time.strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at
    executed_volume = bid_volume
    order_status = 'COMPLETED' # TODO Double check order status
    cmd = "INSERT INTO orders VALUES(" + str(order_id) + \
            ", " + user_id + \
            ", " + str(stock) + \
            ", \"" + type + "\""+\
            ", \"" + created_at + "\""+\
            ", \"" + updated_at + "\""+\
            ", \"" + order_status + "\""+\
            ", " + bid_price + \
            ", " + bid_volume + \
            ", " + executed_volume + \
            ");"
    print(cmd)
    c.execute(cmd)
    r = c.fetchall()
    print('create order insert into db',r)
    db.commit()
    db.close()
    return Response({'Success'}, status=status.HTTP_200_OK)
