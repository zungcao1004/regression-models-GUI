from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression, LogisticRegression
import seaborn as sns 
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor

logr = LogisticRegression()
lr = LinearRegression()
knnr = KNeighborsRegressor()

def x_select(df: DataFrame, columns: tuple):
    x = DataFrame(df, columns=columns)
    return x

def y_select(df: DataFrame, columns: tuple):
    y = DataFrame(df, columns=columns)
    return y

def lr_score(x: DataFrame, y: DataFrame):
    lr.fit(x, y)
    return lr.score(x, y)

def lr_plot(df: DataFrame, x: DataFrame, y: DataFrame):
    if x.columns.size == 2:
        sns.lmplot(df, x= x.columns[0], y=y.columns[0], hue=x.columns[1])
        plt.show()
    elif x.columns.size == 1:
        sns.regplot(df, x=x.columns[0], y=y.columns[0], line_kws=dict(color="r"))
        plt.show()
    else: 
        lr.fit(x, y)
        y_pred = lr.predict(x)
        plt.scatter(y, y_pred)
        plt.xlabel('actual value')
        plt.ylabel('predict value')
        plt.show()
    print('suc')

def logr_score(x: DataFrame, y: DataFrame):
    logr.fit(x, y)
    return logr.score(x, y)

def logr_plot(df: DataFrame, x: DataFrame, y: DataFrame):
    x = x.sort_values(by=x.columns[0])
    sns.regplot(df, x=x.columns[0], y=y.columns[0], logistic=True, ci=None, line_kws=dict(color="r"))
    plt.show()
    print('suc')


def knnr_score(x: DataFrame, y: DataFrame):
    knnr.fit(x, y)
    return knnr.score(x, y)

def knnr_plot(x, y):
    knnr.fit(x, y)
    # Sort x values for better visualization
    x_sorted = x.sort_values(by=x.columns[0])
    y_pred = knnr.predict(x_sorted)
    plt.scatter(x, y, color='blue', label='Data')
    plt.plot(x_sorted, y_pred, color='red', label='KNN Regression')
    plt.xlabel(x.columns[0])
    plt.ylabel(y.columns[0])
    plt.title('KNN Regression')
    plt.legend()
    plt.show()
    print('suc')
