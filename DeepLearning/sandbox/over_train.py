from typing import NamedTuple

from sandbox.multi_layer_net import MultiLayerNet
from sandbox.optimizer import SGD, Adam
from dataset.mnist import load_mnist
import numpy as np
import matplotlib.pyplot as plt

from sandbox.trainer import Trainer


class Net(NamedTuple):
    network: MultiLayerNet
    trainer: Trainer


def train_nets(net: Net):
    net.trainer.train()
    return net.network.weight_decay_lambda, \
           net.trainer.optimizer.lr, \
           net.trainer.train_acc_list, \
           net.trainer.test_acc_list


if __name__ == '__main__':

    (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True)
    x_train = x_train[:500]
    t_train = t_train[:500]

    sample_num = 25
    fig_size = (5, 5)

    nets_list = []
    for n in range(sample_num):
        weight_decay = 10 ** np.random.uniform(-8, -4)
        learning_rates = 10 ** np.random.uniform(-6, -2)
        optimizer = Adam(learning_rates)

        network = MultiLayerNet(784,
                                [100, 100, 100, 100, 100, 100],
                                10, weight_decay_lambda=weight_decay
                                )
        trainer = Trainer(network, x_train, t_train,
                          x_test, t_test, max_epochs=50, optimizer=optimizer)

        nets_list.append(Net(network=network, trainer=trainer))
    from multiprocessing import Pool

    p = Pool(3)
    results = p.map(train_nets, nets_list)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(ncols=fig_size[1], nrows=fig_size[0])
    for r, ax in zip(results, axes.flat):
        ax.plot(range(len(r[2])), r[2])
        ax.plot(range(len(r[3])), r[3])
        ax.set_title(f"w: {r[0]:.2e}\tt: {r[1]:.2e}")
        ax.set_ylim(0.0, 1.0)
        ax.set_xticklabels([])

    plt.show()
