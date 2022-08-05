use tu;

DROP TABLE IF EXISTS ohlcv, market_day, orders, holdings, users, stocks, sectors;
CREATE TABLE sectors(id INT NOT NULL,
          name VARCHAR(50) NOT NULL,
          description VARCHAR(200) NOT NULL,
  	PRIMARY KEY (id)
);

CREATE TABLE stocks(id INT NOT NULL,
          sector_id INT NOT NULL,
          name VARCHAR(20) NOT NULL,
          total_volume INT NOT NULL,
          unallocated INT NOT NULL,
          price NUMERIC NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (sector_id) REFERENCES sectors(id)
);

CREATE TABLE users(id INT NOT NULL,
          name VARCHAR(50) NOT NULL,
          email VARCHAR(50) NOT NULL,
	  password VARCHAR(200) NOT NULL,
          available_funds NUMERIC NOT NULL,
          blocked_funds NUMERIC NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (email),
	UNIQUE (name)
);


CREATE TABLE holdings(user_id INT NOT NULL,
          stock_id INT NOT NULL,
          bought_on date NOT NULL,
          volume INT NOT NULL,
          bld_price NUMERIC NOT NULL,
	id INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (stock_id) REFERENCES stocks(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE orders(id INT NOT NULL,
	user_id INT NOT NULL,
          stock_id INT NOT NULL,
          type VARCHAR(4) NOT NULL,
          create_at date NOT NULL,
          updated_at date NOT NULL,
          status VARCHAR(20) NOT NULL,
          bld_volume INT NOT NULL,
          executed_volume INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (stock_id) REFERENCES stocks(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE market_day(
	id INT NOT NULL,
day INT NOT NULL,
status VARCHAR(10),
PRIMARY KEY (id)
);

CREATE TABLE ohlcv(
	market_id INT NOT NULL,
        stock_id INT NOT NULL,
	open INT NOT NULL,
	high INT NOT NULL,
	low INT NOT NULL,
	close INT NOT NULL,
	volume INT NOT NULL,
	FOREIGN KEY (market_id) REFERENCES market_day(id),
	FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

