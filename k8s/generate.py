import requests

url='http://k8s-tu2k22-zhiyuani-821235eab0-1328227602.us-east-1.elb.amazonaws.com/api/v1/sectors'

while True:
    requests.get(url)
