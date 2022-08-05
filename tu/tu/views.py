from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import backend as bk
import time
from rest_framework.views import APIView

@api_view(['POST'])
def register(request):
    r = str(request.body)[2:-1].split('&')
    print(r)

    if 'email' not in str(request.body) or 'password' not in str(request.body):
        return Response("email not found", status=status.HTTP_400_BAD_REQUEST)
    try:
      email = r[0].split('=')[1]
      pw = r[1].split('=')[1]
      res = bk.register(email, pw)
      print(res)
      return Response(res, status=status.HTTP_201_CREATED)
    except Exception as e:
      print("Invalid User info")
      print(e)
      return Response('Invalid user info', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def loginInfo(request):
    #r = str(request.body)[2:-1].split('&')
    #print(r)

    try:
        res = bk.getLoginSession(email, pw)
        return Response(res, status=status.HTTP_201_CREATED)
    except Exception as e:
      print("Invalid User info")
      print(e)
      return Response('Invalid user info', status=status.HTTP_401_UNAUTHORIZED)
