import numpy as np
import matplotlib.pylab as plt

def _gate(w: np.ndarray, b, x1, x2):
    x = np.array([x1, x2])
    tmp = sum(x * w) + b
    if tmp <= 0:
        return 0
    else:
        return 1


def AND(x1, x2):
    return _gate(np.array([0.5, 0.5]), -0.7, x1, x2)


def NAND(x1, x2):
    return _gate(np.array([-0.5, -0.5]), 0.7, x1, x2)


def OR(x1, x2):
    return _gate(np.array([0.5, 0.5]), -0.2, x1, x2)


def XOR(x1, x2):
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    y = AND(s1, s2)
    return y


def step_function(x: np.ndarray):
    return np.array(x > 0, dtype=np.int)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

if __name__ == '__main__':
    x = np.arange(-5.0, 5.0, 0.1)
    y1 = step_function(x)
    y2 = sigmoid(x)
    y3 = relu(x)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.ylim(-0.1, 1.1)
    plt.show()