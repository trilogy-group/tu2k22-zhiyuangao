
sudo apt update
sudo apt install mysql-server
#sudo service mysql start
sudo mysqld --skip-grant-tables
#GIT_SSH_COMMAND='ssh -i /workspace/tu2k22-zhiyuangao/tu/id_trilogy -o IdentitiesOnly=yes'
# CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
# FLUSH PRIVILEGES;
# 
