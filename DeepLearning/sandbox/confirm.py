from conv_layer_net import SimpleConvNet
from dataset.mnist import load_mnist
import matplotlib.pyplot as plt
import pickle
import gc

(_, _), (x_test, t_test) = load_mnist(normalize=True, flatten=False)

hist = []

for i in range(1, 51):
    with open(f"cnn_networks/network{i}.pkl", 'rb') as f:
        obj: SimpleConvNet = pickle.load(f)
        print(f"predicting{i}")
        hist.append(obj.accuracy(x_test,t_test))
        gc.collect()

plt.plot(range(len(hist)), hist)
plt.show()
