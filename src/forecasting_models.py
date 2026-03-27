from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm


def train_linear_regression(X_train, y_train):

    model = LinearRegression()

    model.fit(X_train, y_train)

    return model