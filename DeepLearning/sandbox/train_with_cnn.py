from typing import NamedTuple

from conv_layer_net import SimpleConvNet
from sandbox.optimizer import SGD, Adam
from dataset.mnist import load_mnist
import numpy as np
import matplotlib.pyplot as plt

from sandbox.trainer import Trainer

(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, flatten=False)

network = SimpleConvNet(x_train[0].shape)
optimizer = Adam()
trainer = Trainer(network, x_train, t_train, x_test, t_test, optimizer=optimizer)
trainer.train()
trainer.show_graph(is_accuracy=False)
import pickle
pickle.dump(trainer, "trainer.pkl")
print("finished")
