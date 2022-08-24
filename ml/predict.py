import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import utils
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn import svm
from sklearn.linear_model import SGDOneClassSVM
from xgboost import XGBRegressor


def rmse_score(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


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

    X_test = np.array(list(range(len(test)))).reshape(-1,1)
    y_test = test.values.ravel()
    Y_pred = linear_regressor.predict(X_test)
    mse = mean_squared_error(Y_pred, y_test)
    mae = mean_absolute_error(Y_pred, y_test)
    rmse = rmse_score(Y_pred, y_test)
    r2 = r2_score(Y_pred, y_test)
    return {'mse':mse,'mae':mae,'rmse':rmse,'r2':r2}


def random_forest(train, validate, test):
    X_train = np.array(list(range(len(train)))).reshape(-1,1)
    X_test = np.array(list(range(len(test)+1))).reshape(-1,1)
    y_train = train.values.ravel()
    y_test = test.values.ravel()

    # 10 trees
    regressor = RandomForestRegressor(n_estimators=10, random_state=0)
    regressor.fit(X_train, y_train)

    # Visualizing
    X_axis = np.arange(min(X_train), max(X_train), 1)
    X_axis = X_axis.reshape(len(X_axis), 1)
    Y_pred = regressor.predict(X_axis)
 
    plt.scatter(X_train, y_train, color='red')
    plt.xlabel("Days")
    plt.ylabel("Growth")
    plt.plot(X_axis, Y_pred, color='blue')
    plt.title('Random Forest Regression')
    plt.show()

    # MSE of test set
    X_axis = np.arange(min(X_test), max(X_test), 1)
    X_axis = X_axis.reshape(len(X_axis), 1)
    Y_pred = regressor.predict(X_axis)
    mse = mean_squared_error(Y_pred, y_test)
    mae = mean_absolute_error(Y_pred, y_test)
    rmse = rmse_score(Y_pred, y_test)
    r2 = r2_score(Y_pred, y_test)
    return {'mse':mse,'mae':mae,'rmse':rmse,'r2':r2}


def xgb_regression(train, validate, test):
    X_train = np.array(list(range(len(train)))).reshape(-1,1)
    X_test = np.array(list(range(len(test)+1))).reshape(-1,1)
    y_train = train.values.ravel()
    y_test = test.values.ravel()

    model = XGBRegressor()
    model.fit(X_train, y_train)

    # Visualizing
    X_axis = np.arange(min(X_train), max(X_train), 1)
    X_axis = X_axis.reshape(len(X_axis), 1)
    Y_pred = model.predict(X_axis)
 
    plt.scatter(X_train, y_train, color='red')
    plt.xlabel("Days")
    plt.ylabel("Growth")
    plt.plot(X_axis, Y_pred, color='blue')
    plt.title('XGB Regression')
    plt.show()

    # MSE
    X_axis = np.arange(min(X_test), max(X_test), 1)
    X_axis = X_axis.reshape(len(X_axis), 1)
    Y_pred = model.predict(X_axis)
    mse = mean_squared_error(Y_pred, y_test)
    mae = mean_absolute_error(Y_pred, y_test)
    rmse = rmse_score(Y_pred, y_test)
    r2 = r2_score(Y_pred, y_test)
    return {'mse':mse,'mae':mae,'rmse':rmse,'r2':r2}


def svm_regression(train, validate, test):
    lab_enc = preprocessing.LabelEncoder()

    X_train = np.array(list(range(len(train)))).reshape(-1,1)
    X_test = np.array(list(range(len(test)+1))).reshape(-1,1)
    y_train = lab_enc.fit_transform(train.values.ravel())
    y_test = test.values.ravel()

    C = 1.0  # SVM regularization parameter
    nu = 0.05
    gamma = 2.0
    #clf = SGDOneClassSVM(nu=nu, shuffle=True, fit_intercept=True, tol=1e-4)
    #clf = svm.SVC(kernel="linear", C=C)
    #clf = svm.LinearSVC(C=C, max_iter=10000)
    clf = svm.SVC(kernel="rbf", gamma=0.7, C=C)
    #clf = svm.SVC(kernel="poly", degree=3, gamma="auto", C=C)
    clf.fit(X_train, y_train)

    # cross-validate
    X_validate = np.array(list(range(len(validate)))).reshape(-1,1)
    y_validate = lab_enc.fit_transform(validate.values.ravel())
    cv = KFold(n_splits=10, random_state=1, shuffle=True)
    scores = cross_val_score(clf, X_validate, y_validate, cv=cv)

    # predict training set
    X_axis = np.arange(min(X_train), max(X_train), 1)
    X_axis = X_axis.reshape(len(X_axis), 1)

    Y_pred = clf.predict(X_axis)

    # predict test set
    X_axis_test = np.arange(min(X_test), max(X_test), 1)
    X_axis_test = X_axis_test.reshape(len(X_axis_test), 1)

    Y_pred_test = clf.predict(X_axis_test)
    n_error_train = Y_pred[Y_pred == -1].size
    n_error_test = Y_pred_test[Y_pred_test == -1].size

    plt.scatter(X_train, y_train, color='red')
    plt.xlabel("Days")
    plt.ylabel("Growth")
    plt.plot(X_axis, Y_pred, color='blue')
    plt.title('SVM')
    plt.show()
    mse = mean_squared_error(Y_pred_test, y_test)
    mae = mean_absolute_error(Y_pred_test, y_test)
    rmse = rmse_score(Y_pred_test, y_test)
    r2 = r2_score(Y_pred_test, y_test)
    return {'mse':mse,'mae':mae,'rmse':rmse,'r2':r2}


def get_sma(prices, rate):
    return prices.rolling(rate).mean()


def stock_preprocess(df):
    df = df.fillna(0)
    rate = 5
    # find sma
    sma = get_sma(df, rate).fillna(0)
    # find bollinger brands
    std = df.rolling(rate).std().fillna(0)
    bollinger_up = sma + std * 2
    bollinger_down = sma - std * 2
    #print(bollinger_up)
    return bollinger_up - bollinger_down


def predict(name, change):
    df = pd.DataFrame(change, columns = ['change'])
    # Milestone 2 
    # Step 1 preprocessing
    df = stock_preprocess(df['change'])
    
    # Step 2 Split
    train, validate, test = \
              np.split(df.sample(frac=1, random_state=42),
                       [int(.6*len(df)), int(.8*len(df))])

    # Step 3.a Linear Regression
    err_lr = linear_regression(train, validate, test)
    #print('Linear regressor error:' + str(err_lr))

    # Step 3.b Random Forest regressor
    err_rfr = random_forest(train, validate, test)
    #print('Random forest error:' + str(err_rfr))

    # Step 3.c XGB regression
    err_xgb = xgb_regression(train, validate, test)
    #print(err_xgb)

    # Step 3.d SVM
    err_svm = svm_regression(train, validate, test)

    # Step 4. box plot
    modelerr = pd.DataFrame()
    modelerr['RMSE'] = [err_lr['rmse'], err_rfr['rmse'], err_xgb['rmse'], err_svm['rmse']]
    modelerr['MAE'] = [err_lr['mae'], err_rfr['mae'], err_xgb['mae'], err_svm['mae']]
    modelerr['R2'] = [err_lr['r2'], err_rfr['r2'], err_xgb['r2'], err_svm['r2']]
    modelerr.rename(index = {0:"LR"}, inplace=True)
    modelerr.rename(index = {1:"RF"}, inplace=True)
    modelerr.rename(index = {2:"SVM"}, inplace=True)
    modelerr.rename(index = {3:"XGB"}, inplace=True)
    modelerr.iloc[::,0:1].boxplot()
    plt.show()
    modelerr.iloc[::,1:2].boxplot()
    plt.show()
    modelerr.iloc[::,2:3].boxplot()
    plt.show()

    # Step 5. Predict already done
