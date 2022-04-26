from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

import numpy as np
import matplotlib.pyplot as plt


def model_selector(x, y):
    threshold = 0.8
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

    X = np.array(X_train)[:, np.newaxis]
    y = np.array(y_train)
    liner_score, liner_reg = _fit_liner(X, y)
    poly_score, poly_reg, quadratic = _fit_poly(X, y)
    print(liner_score)
    print(poly_score)
    # if liner_score >= threshold:
    #     rsult_score = liner_score
    # else:
    #     log_r = _fit_log(X, y)
    #     exp_r = _fit_exp(X, y)
    #     if log_r >= threshold and exp_r >= threshold:
    #         if log_r > exp_r:
    #             return log_r
    #         return exp_r
    #     if log_r >= threshold:
    #         return log_r
    #     if exp_r >= threshold:
    #         return exp_r
    #     rsult_score = poly_score

    _show_chart(liner_reg, poly_reg, quadratic, X_train, y_train, X_test, y_test)


def _fit_liner(X, y):
    liner_reg = linear_model.LinearRegression()
    liner_reg.fit(X, y)

    return liner_reg.score(X, y), liner_reg


def _fit_log(X, y):
    pass


def _fit_exp(X, y):
    pass


def _fit_poly(X, y):
    poly_reg = linear_model.LinearRegression()
    quadratic = PolynomialFeatures(degree=2)
    x_quad = quadratic.fit_transform(X)

    poly_reg.fit(x_quad, y)

    return poly_reg.score(x_quad, y), poly_reg, quadratic


def _show_chart(liner_reg, poly_reg, quadratic, train_x, train_y, test_x, test_y):
    X_fit = np.array(test_x)[:, np.newaxis]
    y_lin_fit = liner_reg.predict(X_fit)
    y_quad_fit = poly_reg.predict(quadratic.fit_transform(X_fit))
    # plot
    plt.scatter(train_x, train_y, color='green', label='training points')
    plt.scatter(test_x, test_y, color='red', label='test points')
    plt.plot(X_fit, y_lin_fit, label='line')
    plt.plot(X_fit, y_quad_fit, label='poly')
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    X = [258.0, 270.0, 294.0, 320.0, 342.0, 368.0, 396.0, 446.0, 480.0, 586.0]
    y = [236.4, 234.4, 252.8, 298.6, 314.2, 342.2, 360.8, 368.0, 391.2, 390.8]

    model_selector(X, y, 0.8)
