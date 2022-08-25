#sudo service mysql restart
#mysqld --skip-grant-table &
mysql < ./create_db.sql
python3 manage.py runserver 
