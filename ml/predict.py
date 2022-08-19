import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


def linear_regression(train, validate, test):
    X = np.array(list(range(len(train)))).reshape(-1,1)
    Y = train.values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    plt.scatter(X, Y)
    plt.xlabel("Days")
    plt.ylabel("Growth")
    plt.plot(X, Y_pred, color='red')
    plt.show()


def random_forest(train, validate, test):
    X_train = np.array(list(range(len(train)))).reshape(-1,1)
    X_test = np.array(list(range(len(test)))).reshape(-1,1)
    y_train = train
    y_test = test

    # 10 trees
    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X_train, y_train)

    # Visualizing
    X_axis = np.arange(min(X_train), max(X_train), 0.01)
    X_axis = X_axis.reshape(len(X_axis), 1)
    plt.scatter(X_train, y_train, colo='red')
    Y_pred = regressor.predict(X_axis)
    plt.plot(X_axis, Y_pred, color='blue')
    plt.title('Random Forest Regression')


def xgb_regression(train, validate, test):
    d
def predict(name, change):
    df = pd.DataFrame(change, columns = ['change'])
    # Milestone 2 
    # Step 1 preprocessing
    print('Wait for you Ian')
    
    # Step 2 Split
    train, validate, test = \
              np.split(df.sample(frac=1, random_state=42),
                       [int(.6*len(df)), int(.8*len(df))])

    # Step 3.a Linear Regression
    linear_regression(train, validate, test)

    # Step 3.b Random Forest regressor
    random_forest(train, validate, test)

    xgb_regression(train, validate, test)

