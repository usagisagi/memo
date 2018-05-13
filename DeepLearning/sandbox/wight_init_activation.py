import numpy as np
import matplotlib.pyplot as plt

from sandbox.ch02_03.ch2 import relu
from sandbox.func import sigmoid

SEED = 42

r = np.random.RandomState(SEED)

x = r.randn(1000, 100)
node_num = 100
hidden_layer_size = 5
init_p = np.sqrt(2.0 / node_num)
activations = {}

for i in range(hidden_layer_size):
    if i != 0:
        x = activations[i - 1]

    w =np.random.randn(node_num, node_num) * init_p
    z = np.dot(x, w)
    a = relu(z)

    activations[i] = a

for i, a in activations.items():
    plt.subplot(1, len(activations), i+1)
    plt.title(str(i+1) + "-layer")
    plt.hist(a.flatten(), 30, range=(0,1))
    plt.ylim(1, 4000)


plt.show()
