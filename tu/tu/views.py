from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import backend as bk
import time, subprocess
from rest_framework.views import APIView
import logging, json
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor

#trace.set_tracer_provider(
#TracerProvider(
#        resource=Resource.create({SERVICE_NAME: "my-helloworld-service"})
#    )
#)
#tracer = trace.get_tracer(__name__)
#LoggingInstrumentor().instrument(set_logging_format=True)
#LoggingInstrumentor(logging_format='%(msg)s [span_id=%(span_id)s]')


# create a JaegerExporter
#jaeger_exporter = JaegerExporter(
    # configure agent
#    agent_host_name='localhost',
#    agent_port=6831,
#    collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift'
#)

# Create a BatchSpanProcessor and add the exporter to it
#span_processor = BatchSpanProcessor()
# add to the tracer
#trace.get_tracer_provider().add_span_processor(span_processor)

@api_view(['GET'])
def logtest(request):
    logger = logging.getLogger(__name__)
    logger.info('----test----')
    """
    with tracer.start_as_current_span("client"):
        try:
            x = 1 / 0
        except Exception as ex:
            pass
    """
    return Response({}, status=status.HTTP_200_OK)


@api_view(['POST'])
def processlogs(request):
    print(request.body)
    try:
        in_json = json.loads(str(request.body).strip('b\''))
        files = in_json['logFiles']
        poolsize = in_json['parallelFileProcessingCount']
        if poolsize < 1:
            raise Exception
    except:
        return Response({"bad requestbad requestbad request"}, status=status.HTTP_400_BAD_REQUEST)
    data = bk.processLogs(files, int(poolsize))

    return data


@api_view(['POST'])
def register(request):
    logging.getLogger().setLevel(logging.CRITICAL)
    logging.debug('\n-- sign up new user --')
    logging.debug(request.body)
    logging.debug(str(request.body)[1:])
    s = str(request.body)[3:-2]#.strip('{}')
    r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
 
    logging.debug('parsed request')
    print(r)
    logging.info(r)

    if 'email' not in str(request.body) or 'password' not in str(request.body) \
            or 'name' not in str(request.body):
        return Response("email, password or name not found", status=status.HTTP_400_BAD_REQUEST)
    logging.debug('parameters are correct')
    try:
      dic = {}
      for param in r:
          dic[param.split(':')[0]] = param.split(':')[1]
      logging.info(dic)
 
      # assume there are no = in names
      # assume there are no = in password
 
      email = dic['email']
      pw = dic['password']
      name = dic['name']
      print(email, pw, name)
      res = bk.register(email, pw, name)
      logging.debug(res)
      return Response(res, status=status.HTTP_201_CREATED)
    except Exception as e:
      print("User sign-up failed")
      print(e)
      return Response('User sign-up failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    logging.debug(request.body)
    s = str(request.body)[3:-2]#.strip('{}')
    r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
 
    logging.info("login")
    logging.info(str(r))

    if 'email' not in str(request.body) or 'password' not in str(request.body):
        return Response("email or password not found", status=status.HTTP_400_BAD_REQUEST)

    try:
        dic = {}
        for param in r:
            dic[param.split(':')[0]] = param.split(':')[1]
        res = bk.login(dic['email'], dic['password'])
        if res[0] == True:
            return Response(res[1], status=status.HTTP_200_OK)
        else:
            return Response("Wrong username or password", status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Login failed.")
        print(e)
        return Response('Login failed. Check your username and password', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def logout(request):
    try:
        logging.debug('Send log out request to backend')
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        return bk.logout(token)
    except Exception as e:
        logging.debug('token request failed       ')
        print("Logout failed.")
        print(e)
        return Response('Logout failed. Wrong token.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def profile(request):
    logging.debug(request.body)
    s = str(request.body)[3:-2]#.strip('{}')
    r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").split(',')
 
    logging.info("profile")
    logging.info(r)

    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
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
            #token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            return bk.sectorsGet()
        except Exception as e:
            print("GET sectors failed")
            print(e)
            return Response("GET sectors failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':

        logging.debug(request.body)
        s = str(request.body)[3:-2]#.strip('{}')
        r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
        logging.info("sector post")
        logging.info(r)

        #print("sectors", r)
        if 'name' not in str(request.body) or 'description' not in str(request.body):
            logging.debug("description or name not found")
            return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)

        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            logging.debug('Got token')
            if token == None:
                raise Exception
        except Exception as e:
            logging.debug("Need token to proceed")
            return Response("Need token to proceed", status=status.HTTP_401_UNAUTHORIZED)
 
        try:
          dic = {}
          for param in r:
              logging.debug(param)
              dic[param.split(':')[0]] = param.split(':')[1]
 
          des = dic['description']
          name = dic['name']
          res = bk.sectorsPost(description=des, name=name, token=token)
          return res #Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
          print("Sector creation failed")
          print(e)
          return Response('Sector creation failed', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH', 'GET'])
def sectorsUpdate(request, id=None, *args, **kwargs):
    if request.method == 'GET':
        print('sectors get!')
        try:
            #token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            return bk.sectorsGetById(int(id))
        except Exception as e:
            print("GET sectors failed")
            print(e)
            return Response("GET sectors failed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        #if 'name' not in str(request.body) or 'description' not in str(request.body):
        #    logging.debug(str(request.body))
        #    logging.debug('description or name not found')
        #    return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            print('sector patch')
            if token == None:
                raise Exception
        except Exception as e:
            logging.debug('Get Token Error')
            return Response("Need token to proceed", status=status.HTTP_401_UNAUTHORIZED)
 
        try:
            s = str(request.body)[3:-2]#.strip('{}')
            r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").split(',')
 
            dic = {}
            for param in r:
                dic[param.split(':')[0]] = param.split(':')[1]
            print(dic)
 
            if 'description' in dic:
                des = dic['description']
            else:
                des = None
            if 'name' in dic:
                name = dic['name']
            else:
                name = None
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
        logging.debug('\nget all stocks')
        try:
            res = bk.listStocks()
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Failed to get stocks", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'POST':
        print('create stocks')
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            if token == None:
                raise Exception
        except Exception as e:
            return Response("Need token to proceed", status=status.HTTP_401_UNAUTHORIZED)
 
        try:
            if 'name' not in str(request.body) or \
                   'price' not in str(request.body) or 'sector' not in str(request.body) or \
                   "unallocated" not in str(request.body) or 'total_volume' not in str(request.body):
                logging.debug(str(request.body))
                logging.debug('parameter not found')
                return Response("description or name not found", status=status.HTTP_400_BAD_REQUEST)
            s = str(request.body)[3:-2]#.strip('{}')
            r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
 
            dic = {}
            for param in r:
                dic[param.split(':')[0]] = param.split(':')[1]

            logging.info('Here')
            print(dic)
            res = bk.stocksCreate(name=dic['name'], price=dic['price'], sector_id=dic['sector'], \
                    unallocated=dic['unallocated'], total_volume=dic['total_volume'], token=token)
            return res #Response(res, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response("Failed to update stocks", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getStockById(request, id=None):
    """
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        if token == None:
            raise Exception
    except Exception as e:
        token = None
        logging.debug('no token but fine')
        pass
        #return Response("", status=status.HTTP_401_UNAUTHORIZED)
    """
 
    try:
        logging.debug('Got token!')
        res = bk.getStockById(int(id))
        return res
    except Exception as e:
        logging.debug('bk getStockById exception')
        print(e)
        return Response("Failed to get stock by id "+str(id), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def orders(request):
    print('\n\n---- order ---- ')
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        if token == None:
            raise Exception
        logging.debug('GOT Token')
    except Exception as e:
        logging.debug('No Token')
        return Response("Need token to proceed", status=status.HTTP_401_UNAUTHORIZED)
 
    if request.method == "GET":
        # List all orders
        try:
            res = bk.getOrders(token)
            return res
        except Exception as e:
            print(e)
            return Response("Failed to get order", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        print('Post an order')
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        print(token)
        if token == '':
            return Response("token not found", status=status.HTTP_400_BAD_REQUEST)
        try:
            s = str(request.body)[3:-2]#.strip('{}')
            r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
 
            print('order input:'+str(r))
            dic = {}
            for param in r:
                dic[param.split(':')[0]] = param.split(':')[1]
            print(dic)
            res = bk.ordersCreate(stock=dic['stock'], type=dic['type'], \
                    bid_price=dic['bid_price'], \
                    bid_volume=dic['bid_volume'], token=token)
            return res
        except Exception as e:
            print(e)
            return Response("Failed to create order", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 


@api_view(['GET'])
def match(request):
    return Response('TODO', status=status.HTTP_200_OK)
    logging.info('\n\n---- MATCH ---- ')
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        if token == None:
            raise Exception
        logging.debug('GOT Token')
    except Exception as e:
        logging.debug('No Token')
        return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)

    res = bk.match()
    return res
 

@api_view(['POST'])
def open(request):
    return Response('', status=status.HTTP_200_OK)
    logging.info('\n\n---- OPEN ---- ')
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        if token == None:
            raise Exception
        logging.debug('GOT Token')
    except Exception as e:
        logging.debug('No Token')
        return Response("Need token to proceed", status=status.HTTP_400_BAD_REQUEST)

    res = bk.openMarket()
    return res
 


@api_view(['POST'])
def githublogin(request):
        return Response(status.HTTP_200_OK)
        s = str(request.body)[3:-2]#.strip('{}')
        r = s.replace(': ', ':').replace(", ", ",").replace("\"", "").replace('\\','').split(',')
        print('order input:'+str(r))
        dic = {}
        for param in r:
            dic[param.split(':')[0]] = param.split(':')[1]
        print(dic)
        
        code = dic['code']
        print(f"Got code {code} from github")
        client_id = '493h919dqbnrkf89j96jatus0i'
        client_secret = 'kc1tje3b9po84tjp01qdqrb85ppvg30o8b16qihnk3ffs9mfahf'
        redirect_url = 'https://8080-trilogygrou-tu2k22zhiyu-sq8b22pxndn.ws.legacy.devspaces.com/login.html'
        r = requests.post(f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&redirect_url={redirect_url}')
        token = str(r.content)[15:-26]

        response_get_user = requests.get('https://api.github.com/user',  headers={"Authorization":f"token {token}"})
        user_raw = response_get_user.content
        user_parsed = json.loads(user_raw)
        new_username = user_parsed.get('login')
        new_email = user_parsed.get('email')
        print(new_email,new_username)

        if not User.objects.all().filter(username=new_username).exists():
            if new_email and new_username:
                user = User.objects.create(username=new_username, password=token, email=new_email, github_token=token)
                auth_token = Token.objects.create(user=user)
            else:
                user = User.objects.create(username=new_username, password=token, email='none', github_token=token)
        else:
            User.objects.all().get(username=new_username)

        logger.info("Got token back from github: ", token)
        logger.info("Created new user with GitHub information.")
        return Response(status.HTTP_200_OK)
