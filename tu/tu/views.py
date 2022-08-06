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

    if 'token' not in str(request.body):
        return Response("token not found", status=status.HTTP_400_BAD_REQUEST)

    try:
        dic = {}
        for param in r:
            dic[param.split('=')[0]] = param.split('=')[1]
 
        return Response(bk.logout(token=dic['token']), status=status.HTTP_200_OK)
    except Exception as e:
        print("Logout failed.")
        print(e)
        return Response('Logout failed. Wrong token.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def profile(request):
    r = str(request.body)[2:-1].split('&')
    print("profile",r)

    if 'token' not in str(request.body):
        return Response("token not found", status=status.HTTP_400_BAD_REQUEST)

    try:
        dic = {}
        for param in r:
            dic[param.split('=')[0]] = param.split('=')[1]
 
        res = bk.profile(dic['token'])
        return Response(res, status=status.HTTP_200_OK)
    except Exception as e:
        print("Logout failed.")
        print(e)
        return Response('Profile access failed. Wrong token.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def sectors(request):
    if request.method == 'GET':
        try:
            res = bk.sectorsGet()
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print("GET sectors failed")
            print(e)
            return Response("GET sectors failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        r = str(request.body)[2:-1].split('&')
        #print("sectors", r)
        if 'name' not in str(request.body) or 'description' not in str(request.body):
            return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
        try:
          dic = {}
          for param in r:
              dic[param.split('=')[0]] = param.split('=')[1]
 
          des = dic['description']
          name = dic['name']
          res = bk.sectorsPost(description=des, name=name)
          #print(res)
          return Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
          print("Sector creation failed")
          print(e)
          return Response('Sector creation failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
def sectorsUpdate(request, id=None, *args, **kwargs):
    if 'name' not in str(request.body) or 'description' not in str(request.body):
            return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
    try:
        r = str(request.body)[2:-1].split('&')
        dic = {}
        for param in r:
            dic[param.split('=')[0]] = param.split('=')[1]

        des = dic['description']
        name = dic['name']
        print('sectors update', type(id))
        res = bk.sectorsUpdate(int(id), name, des)
        return res 
    except Exception as e:
        print("Sector update failed")
        print(e)
        return Response('Sector update failed', status=status.HTTP_401_UNAUTHORIZED)


