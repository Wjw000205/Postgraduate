import numpy as np
import matplotlib.pyplot as plt


def linear_regression(X, y):
    """
    线性回归函数，接受X和y作为参数进行拟合。
    X: 横坐标数组（自变量）
    y: 纵坐标数组（因变量）

    返回回归系数 theta 和预测值 y_predict。
    """
    # 确保 X 和 y 是 numpy 数组
    X = np.array(X)
    y = np.array(y)

    # 添加偏置项（1列）
    X_b = np.c_[np.ones((len(X), 1)), X]

    # 计算回归系数
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

    # 预测结果
    y_predict = X_b.dot(theta_best)

    # 可视化
    plt.scatter(X, y, color='blue', label='Data points')  # 原始数据点
    plt.plot(X, y_predict, color='red', label='Fitted line')  # 拟合的回归线
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('Linear Regression - Least Squares Fit')

    # 在图表上显示回归系数和预测结果
    plt.text(sum(X)/len(X), max(y), f"θ0: {theta_best[0]:.2f}, θ1: {theta_best[1]:.2f}",
             fontsize=12, color='green', ha='center')

    plt.legend()
    plt.show()

    # 返回回归系数和预测值
    return theta_best, y_predict
