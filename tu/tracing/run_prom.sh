docker run \
    ---net=host \
    -v /home/zgao/Doc/TU/tu2k22-zhiyuangao/tu/tracing/prometheus_django.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus

#-p 9090:9090 \
