import requests
import MySQLdb
import secrets
import json
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
    def __init__(self, name, token, db_entry_in_users):
        self.username = name
        self.data = {'id':db_entry_in_users[0], \
                'name':db_entry_in_users[1], \
                'email':db_entry_in_users[2], \
                'password':db_entry_in_users[3], \
                'availble_funds': int(str(db_entry_in_users[4]).strip('Decimal(\')')), \
                'blocked_funds': int(str(db_entry_in_users[5]).strip('Decimal(\')')) \
            }
        self.token = token


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
    print(r)
    r = c.fetchall()[0][0]
    user_id = int(r) + 1

    cmd = "INSERT INTO users \n\
            VALUES (" + str(user_id) + \
            ", \"" + name + "\"" +\
            ", \"" + email + "\"" + \
            ", \"" + password + "\"" + \
            ", "+ str(40000) + \
            ", "+ str(0) + ");"
    #print(cmd)
    c.execute(cmd)
    #print(c.fetchall())
    db.commit()
    db.close()

    return {"id":user_id}


def login(name, password):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE name =\"" + name+"\"")
    # e.g., ((1, 'zhiyuan', 'string3', 'string', Decimal('40000'), Decimal('0')),)
    r = c.fetchall()[0] # username not found -> raise tuple index error -> exception caught in views
    #print(r)
    if r[3] == password:
        token = secrets.token_urlsafe().strip('=')
        session = Session(name, token, r)
        login_session[token] = session

        db.close()
        return (True, {"token": token})
    else:
        db.close()
        return (False, {"token": "wrong"})


def logout(token):
    del login_session[token]
    return {"logout":"success"}


def profile(token):
    print(login_session, token)
    data = login_session[token].data
    for k in data:
        data[k] = str(data[k])
    return data


def sectorsGet():
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM sectors")
    r = c.fetchall()
    if len(r) == 0:
        return {"sectors empty"}
    id = r[0][0]
    name = r[0][1]
    description = r[0][2]
    db.close()
    return {'id':id, 'name':name, 'description':description}


def sectorsPost(name, description):
    db = get_connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM sectors;")
    r = c.fetchall()[0][0]
    user_id = int(r) + 1

    cmd = "INSERT INTO sectors \n\
            VALUES (" + str(user_id) + \
            ", \"" + name + "\"" +\
            ", \"" + description + "\");"
    #print(cmd)
    c.execute(cmd)
    #print(c.fetchall())
    db.commit() 
    db.close()

    return {'id': user_id, 'name': name, 'description':description}


def sectorsUpdate(id, name, description):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM sectors WHERE id = "+str(id)+";")
    r = c.fetchall()
    print("select result", r)
    if len(r) == 0:
        return Response({'message':"No sector with id "+str(id)}, status.HTTP_406_NOT_ACCEPTABLE)
    id = r[0][0]
    name = r[0][1]
    
    cmd = "UPDATE sectors set description = \"" + \
            description+"\" WHERE id = "+str(id) + \
            " and name = \"" + name + "\";"
    c.execute(cmd)
    #print(c.fetchall())
    db.commit() 
    db.close()
    return Response({'id':'ok'}, status=status.HTTP_204_NO_CONTENT)


def stocks():
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM stocks;")
    res = []
    r = c.fetchall()
    for stock in r:
        #((1, 1, 'stock1', 100, 100, Decimal('200')), (2, 1, 'stock2', 100, 100, Decimal('200')))
        id = int(stock[0])
        sector_id = int(stock[1])
        name = stock[2]
        total_volume = int(stock[3])
        unallocated = int(stock[4])
        price = float(str(stock[5]).strip("Decimal(\')"))

        data = {"id":id, "name":name, "total_volume":total_volume, "sector":sector_id, \
                "unallocated":unallocated, "price":price}
        res.append(data)
        
    #print(r)
    return res


def stocksCreate(name, price, sector_id, unallocated, total_volume):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT COUNT(*) FROM users;")
    r = c.fetchall()[0][0]
    stock_id = int(r) + 1

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

    return {"id":user_id}


def getStock(id):
    db = get_connect()
    c = db.cursor()

    c.execute("SELECT * FROM stocks WHERE id = "+str(id)+';')
    r = c.fetchall()
    if len(r) == 0:
        return {}
    data = r[0]
    print(data)
    sector_id = data[1]
    name = data[2]
    total_volume = data[3]
    unallocated = data[4]
    price = str(str(data[5]).strip('Decimal(\')'))
    return {'id': id, 'name': name, 'price': price, 'sector': sector_id, 'unallocated': unallocated, \
            'price': price} 