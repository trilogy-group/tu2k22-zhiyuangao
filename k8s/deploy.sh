kubectl create deployment zhiyuan-app --image=zhiyuangao/django:latest
kubectl autoscale deployment zhiyuan-app -n tu2k22 --max 5
