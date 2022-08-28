FROM ubuntu:20.04
RUN apt-get update && apt-get install -y tzdata && apt install -y python3.8 python3-pip
RUN apt-get install mysql-server -y
RUN apt install python3-dev libpq-dev nginx -y
RUN apt install default-libmysqlclient-dev build-essential -y
RUN pip install django django-prometheus djangorestframework opentelemetry-sdk opentelemetry-api opentelemetry-instrumentation opentelemetry-instrumentation-django mysqlclient opentelemetry-exporter-jaeger opentelemetry-exporter-otlp opentelemetry-instrumentation-logging cryptography drf-jwt
ADD . /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
CMD ["bash", "start.sh"]
