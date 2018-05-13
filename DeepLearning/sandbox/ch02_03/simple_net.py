import sys, os
import numpy as np

from sandbox.func import softmax, cross_entropy_error, numerical_gradient

seed = 42


class simpleNet():
    def __init__(self):
        r = np.random.RandomState(seed=seed)
        self.W = r.randn(2, 3)  # 2*3のarrayを作成

    def predict(self, x):
        return np.dot(x, self.W)

    def loss(self, x, t):
        z = self.predict(x)
        y = softmax(z)
        loss = cross_entropy_error(y, t)  # yとtのクロスエントロピーの差

        return loss


if __name__ == '__main__':
    net = simpleNet()
    x = np.array([0.6, 0.9])
    t = np.array([0, 0, 1])
    print(net.loss(x, t))
    def f(W):
        return net.loss(x,t)
    dW = numerical_gradient(f, net.W)
    print(dW)