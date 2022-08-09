from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import backend as bk
import time
from rest_framework.views import APIView

@api_view(['POST'])
def register(request):
    r = str(request.body)[2:-1].split('&')
    print('register',r)

    if 'email' not in str(request.body) or 'password' not in str(request.body) \
            or 'name' not in str(request.body):
        return Response("email, password or name not found", status=status.HTTP_400_BAD_REQUEST)
    try:
      dic = {}
      for param in r:
          dic[param.split('=')[0]] = param.split('=')[1]
 
      # assume there are no = in names
      # assume there are no = in password
 
      email = dic['email']
      pw = dic['password']
      name = dic['name']
      res = bk.register(email, pw, name)
      print(res)
      return Response(res, status=status.HTTP_201_CREATED)
    except Exception as e:
      print("User sign-up failed")
      print(e)
      return Response('User sign-up failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    r = str(request.body)[2:-1].split('&')
    print("login",r)

    if 'username' not in str(request.body) or 'password' not in str(request.body):
        return Response("username or password not found", status=status.HTTP_400_BAD_REQUEST)

    try:
        dic = {}
        for param in r:
            dic[param.split('=')[0]] = param.split('=')[1]
        res = bk.login(dic['username'], dic['password'])
        if res[0] == True:
            return Response(res[1], status=status.HTTP_200_OK)
        else:
            return Response("Wrong username or password", status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print("Login failed.")
        print(e)
        return Response('Login failed. Check your username and password', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def logout(request):
    r = str(request.body)[2:-1].split('&')
    print("logout",r)

    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        return bk.logout(token)
    except Exception as e:
        print("Logout failed.")
        print(e)
        return Response('Logout failed. Wrong token.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def profile(request):
    r = str(request.body)[2:-1].split('&')
    print("profile",r)

    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            raise Exception
    except Exception as e:
            return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
    try:
        res = bk.profile(token)
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        print("Logout failed.")
        print(e)
        return Response('Profile access failed. Wrong token.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def sectors(request):
    if request.method == 'GET':
        print('sectors get!')
        try:
            #token = request.META.get('HTTP_AUTHORIZATION')
            return bk.sectorsGet()
        except Exception as e:
            print("GET sectors failed")
            print(e)
            return Response("GET sectors failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        r = str(request.body)[2:-1].split('&')
        #print("sectors", r)
        if 'name' not in str(request.body) or 'description' not in str(request.body):
            return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token == None:
                raise Exception
        except Exception as e:
            return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
        try:
          dic = {}
          for param in r:
              dic[param.split('=')[0]] = param.split('=')[1]
 
          des = dic['description']
          name = dic['name']
          res = bk.sectorsPost(description=des, name=name, token=token)
          #print(res)
          return res #Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
          print("Sector creation failed")
          print(e)
          return Response('Sector creation failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
def sectorsUpdate(request, id=None, *args, **kwargs):
    if 'name' not in str(request.body) or 'description' not in str(request.body):
            return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            raise Exception
    except Exception as e:
            return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
    try:
        r = str(request.body)[2:-1].split('&')
        dic = {}
        for param in r:
            dic[param.split('=')[0]] = param.split('=')[1]

        des = dic['description']
        name = dic['name']
        print('sectors update', type(id))
        res = bk.sectorsUpdate(int(id), name, des, token=token)
        return res 
    except Exception as e:
        print("Sector update failed")
        print(e)
        return Response('Sector update failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def stocks(request):
    if request.method == 'GET':
        print('get stocks')
        try:
            res = bk.stocks()
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Failed to get stocks", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        print('create stocks')
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token == None:
                raise Exception
        except Exception as e:
            return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
        try:
            r = str(request.body)[2:-1].split('&')
            dic = {}
            for param in r:
                dic[param.split('=')[0]] = param.split('=')[1]
            res = bk.stocksCreate(name=dic['name'], price=dic['price'], sector_id=dic['sector'], \
                    unallocated=dic['unallocated'], total_volume=dic['total_volume'], token=token)
            return res #Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("Failed to update stocks", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getStock(request, id=None):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            raise Exception
    except Exception as e:
        return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
    try:
        res = bk.getStock(int(id), token)
        return res
    except Exception as e:
        print(e)
        return Response("Failed to get stock by id "+str(id), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def orders(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            raise Exception
    except Exception as e:
        return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)
 
    if request.method == "GET":
        # List all orders
        try:
            res = bk.getOrders(token)
            return res
        except Exception as e:
            print(e)
            return Response("Failed to get order", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == '':
            return Response("token not found", status=status.HTTP_400_BAD_REQUEST)
        try:
            r = str(request.body)[2:-1].split('&')
            dic = {}
            for param in r:
                dic[param.split('=')[0]] = param.split('=')[1]
            res = bk.ordersCreate(stock=dic['stock_id'], type=dic['type'], \
                    bid_price=dic['bid_price'], \
                    bid_volume=dic['bid_volume'], token=token)
            return res
        except Exception as e:
            print(e)
            return Response("Failed to create order", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


