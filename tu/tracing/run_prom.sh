docker run \
    -p 9090:9090 \
    -v /home/zgao/Doc/TU/tu2k22-zhiyuangao/tu/tracing/prometheus_django.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus

