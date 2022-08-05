import MySQLdb
import random, time

#db_host = "172.18.64.1"
db_host = "localhost"
db_user = "sammy"
db_name = "tu"
password = "Ab_19100204"
port = 3306

connect_pool=[]

def connectDB():
    connect=MySQLdb.connect(host=db_host,password=password, user=db_user, db=db_name, port=port)
    print("Connected")
    return connect

def get_connect():
    global connect_pool
    if not connect_pool:
        connect_tmp=connectDB()
        connect_pool.append(connect_tmp)
    return connect_pool.pop()

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

def run():
    db = get_connect()
    c = db.cursor()

    # create table
    c.execute("DROP TABLE transactions;")
    c.execute("CREATE TABLE transactions(transactionID INT NOT NULL, \
          company_code VARCHAR(20) NOT NULL, \
          company_name VARCHAR(300) NOT NULL, \
          company_email VARCHAR(300) NOT NULL, \
          date TIMESTAMP NOT NULL, \
          day_high INT NOT NULL, \
          day_low INT NOT NULL, \
          open INT NOT NULL, \
          close INT NOT NULL, \
          volume INT NOT NULL);")

    # insert data
    f = open('nasdaq.csv', 'r')
    lines = list(f.readlines())
    transactionID = 0
    while transactionID < 10001:
        for l in lines[1:101]:
            transactionID += 1
            data = l.split(',')
            company_code = data[0]
            company_name = data[1]
            company_email = 'contact@'+company_name.replace(' ', '')+'.com'
            date = random_date("2022-05-01 01:01:01", "2022-08-04 01:01:01", random.random())
            day_high = random.randint(500, 5000)
            day_low = random.randint(0, day_high)
            open_price = random.randint(day_low, day_high)
            close_price = random.randint(day_low, day_high)
            volume = random.randint(day_high, day_high*1000)

            cmd = "INSERT INTO transactions \n\
                VALUES ("+str(transactionID) + \
                ", \"" + company_code + "\""\
                ", \"" + company_name + "\""\
                ", \"" + company_email + "\""\
                ", \"" + date + "\""\
                ", " + str(day_high) + \
                ", " + str(day_low) + \
                ", " + str(open_price) + \
                ", " + str(close_price) + \
                ", " + str(volume) + ");"
            c.execute(cmd)
            result = c.fetchall()
        db.commit()



    # 1. Find companies that have shown highest percentage growth over the last 100 days
    print("1. Find companies that have shown highest percentage growth over the last 100 days")
    c.execute("\
      select company_name, MAX((close - open)/open*100) AS growth \
      from transactions \
      WHERE transactions.date > now() - INTERVAL 100 day \
      GROUP BY company_name \
      ORDER BY growth LIMIT 5") 
    result = c.fetchall()
    print(result)
    # 2.
    print("\n2. Sort companies in ascending order of average volatility[per day basis: (day_high - day_low)/day_low]")
    c.execute("select company_name, AVG((day_high - day_low)/day_low) AS volatility \
      FROM transactions \
      GROUP BY company_name \
      ORDER BY volatility LIMIT 5")
    result = c.fetchall()
    print(result)
    # 3.
    print("\n3. Name and code of the worst performing(percentage wise) stock over the last 30 days")
    c.execute("select company_name, company_code, MIN((close - open)/open*100) AS growth \
      from transactions \
      WHERE transactions.date > now() - INTERVAL 30 day \
      GROUP BY company_name, company_code \
      ORDER BY growth \
      LIMIT 1 \
            ")
    result = c.fetchall()
    print(result)

    #
    print("\n4. Name and code of company with largest market capitalization at the end of day 30")
    c.execute("\
    select company_name, company_code, date, (close*volume) as market_capitalization \
      from transactions \
    where date = ( select MIN(date) from transactions)\
      ORDER BY market_capitalization \
      LIMIT 1")
    result = c.fetchall()
    print(result)

    #
    print("\n5. Find the date where top 5 companies(based on market cap on last day) showed the most average growth")
    c.execute(" \
        SELECT date, AVG((close - open)/open*100) AS avg_growth \
        FROM transactions \
        WHERE company_name IN ( \
              SELECT company_name FROM ( \
                  SELECT company_name, (close*volume) as market_capitalization \
                  FROM transactions \
                  WHERE date = ( \
                      select MAX(date) as last_day FROM transactions \
                  ) \
                  ORDER BY market_capitalization DESC \
                  LIMIT 5 \
              ) as top_5_companies \
        ) \
        GROUP BY date \
        ORDER BY avg_growth DESC \
        LIMIT 1            \
            ")
    result = c.fetchall()
    print(result)


    f.close()
    db.close()


if __name__=="__main__":
    run()

