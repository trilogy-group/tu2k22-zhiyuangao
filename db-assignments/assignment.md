## Milestone 1.

Given data format
![image](https://user-images.githubusercontent.com/110180090/182682035-e5f76cd4-560c-4684-8c05-3a2a49aa0a29.png)


#### 1NF

According to the definition of the first normal form (1NF), all attributes (columns, fields) of a table must be atomic (indivisible), and that each entry has to be unique.

In the given format, each table cell only contain a single value (atomic), and each record is already unique. So it is already an 1NF.

**Analysis**:

The pros of 1NF:
Before we convert it into 1NF, some attributes contain data sets (arrays).
If we do not implement the division/atomity, then the data can be distorted – if the same data is entered incorrectly, they will be treated as different data.

The cons of 1NF:
We need more space in the table because we have more redundancy.

### 2NF

Our 1NF has a composite primary key – which means multiple columns are combined to uniquely identify each entry in the table, but it does not guarantee uniqueness when taken individually. 

We want to make sure the relevant data stays together. We don’t want StockType, StockTypeID to be in the same entry as the user.

In order to convert to 2NF, we make new tables to eliminate partial dependencies.

Table 1. Primary Key: UserID; Foreign Key, StockID.


![image](https://user-images.githubusercontent.com/110180090/182682142-da726722-d2f0-4c54-b7c6-bf497a4439ac.png)


Table 2. Primary Key: StockID

![image](https://user-images.githubusercontent.com/110180090/182682206-8bad45a1-431d-4414-a754-3e2d6fe6818a.png)

**Analysis**:
Pros: Tables are narrower. Every column is functionally dependent on the primary key.
Cons: Anomalies can still happen. 
Deletion anomaly: If I remove one stock, then in table 1 I can lose data about the stock.
Insertion anomaly: If I insert data in table 1, then table 2 cannot be empty, we need data from table 2 before inserting into table 1.
Modification anomaly: one StockID can be in multiple rows in table 1

### 3NF

A relation is in third normal form, if there is no transitive dependency for non-prime attributes as well as it is in second normal form.

Now we have StockID -> StockName, StockID -> StockType -> StockTypeID which is a transitive relationship (aka. Transitively dependent).

So we should decompose the table 2 in 2NF.

Table 1 same as before.

Table 2-1

![image](https://user-images.githubusercontent.com/110180090/182682375-8d100440-08cf-491c-834b-e302848dd9b4.png)

Table 2-2

![image](https://user-images.githubusercontent.com/110180090/182682444-a236de0d-c668-49b1-8f6a-018491967975.png)

Table 2-3

![image](https://user-images.githubusercontent.com/110180090/182682514-816429df-f589-4540-bff9-d3377567506d.png)

**Analysis**:
Pros: We eliminated the modification anomaly from 2NF.
Cons: We have many tables and joins in between those tables, so we slow down the performance of the database.


## Milestone 2

**ER diagram**

![Entity Relationship Diagram (1)](https://user-images.githubusercontent.com/110180090/182682775-f4abaff9-30b1-4181-bbcb-15dd2621fe52.jpg)

To retrieve holding of UserID 3 
SELECT SUM(Profit) FROM Orders WHERE UserID = 3


## Milestone 3

Assume we are using the ER from milestone 2

#### 1\. Net Volume
\# Note, profit means either buying or selling, so it can be minus
\# Assume StockID = ‘S100’, Day = ‘2022–08-04’
SELECT SUM(ABS(Orders.Amount)) FROM Orders WHERE StockID == ‘S100’ AND Day == ‘2022-08-04’;


#### 2\. Net gains/losses of one user on a given day
\# UserID = U100, Day = ‘2022–08-04’
SELECT SUM(Orders.Amount) FROM Orders WHERE UserID == ‘U100’ AND Day == ‘2022–08-04’;

#### 3\. Top 5 stocks with highest percentage growth last month
I don't know

#### 4\. Average buying price for a stock in a users holdings
\# Assume the stock we looking for is S100, userid is U100
SELECT AVG(Orders.Amount) FROM Orders WHERE StockID = ‘S100’ and UserID = ‘U100’;

#### 5\. Net profit/loss per current holding of a user
\# Because amount can be profit or loss — positive amount or negative amount
SELECT SUM(Orders.Amount) FROM Orders WHERE UserID = ‘U100’;

#### 6\. Top performing stock in a users portfolio in the previous month(percentage growth)




