
sudo apt update
sudo apt install mysql-server
#sudo service mysql start
sudo mysqld --skip-grant-tables
#GIT_SSH_COMMAND='ssh -i /workspace/tu2k22-zhiyuangao/tu/id_trilogy -o IdentitiesOnly=yes'
# CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
# FLUSH PRIVILEGES;
# 
(0, 2, 'Googtles12345', 1000, 1000, Decimal('1000'))
{
  "id": 0,
  "name": "string",
  "price": "100.00",
  "sector": 0,
  "unallocated": 0,
  "total_volume": 0
}

docker build -t gcr.io/micro-harbor-259903/videosharex:v2 .
docker push gcr.io/micro-harbor-259903/videosharex:v3
kubectl create deployment videosharex-app --image=gcr.io/micro-harbor-259903/videosharex:v3
kubectl expose deployment videosharex-app --type=LoadBalancer --port 8000 --target-port 8000
# docker run -i -t --rm -p 8000:8000 xxxx
