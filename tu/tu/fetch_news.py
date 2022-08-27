import os
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import logging

logging.basicConfig(filename="wallstreet_server.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
heimdall = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
heimdall.setLevel(logging.INFO)
heimdall.info("LOG configured")

host = 'search-tu2k22-news-cwsesp2y22pqyu2gkcrlj6or5a.us-east-1.es.amazonaws.com'
region = 'us-east-1'
index_name = 'tu2k22-zhiyuangao-news'
company_names = [
    'Google', 'Microsoft', 'IBM', 'Apple', 'Meta', 'Tesla', 'Amazon', 'Palantir',
    'Adobe', 'Samsung', 'Nvidia', 'Broadcom', 'Oracle', 'Cisco', 'Intel', 'Netflix'
]

session = boto3.Session(
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", 0),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", 0),
    region_name = os.getenv("AWS_REGION", "us-east-1")
)

service = 'es'
credentials = session.get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=None)

client = OpenSearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

def fetch_news(company):
    try:
        query = {
            'size': 10,
            'query': {
                'match': {
                'company': company
                }
            }
        }

        response = client.search(
            body = query,
            index = index_name
        )

        news_collection = []

        for news in response['hits']['hits']:
            news_collection.append(news['_source'])

    except Exception as ex:
        print(ex)
        heimdall.info(str(ex))
        return []

    return news_collection

#print(fetch_news('Google'))
