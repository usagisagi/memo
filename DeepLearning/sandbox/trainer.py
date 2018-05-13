import numpy as np

from sandbox.multi_layer_net import MultiLayerNet
from sandbox.optimizer import Optimizer, SGD
import pickle

class Trainer:
    def __init__(self,
                 network,
                 x_train: np.array,
                 t_train: np.array,
                 x_val: np.array,
                 t_val: np.array,
                 optimizer: Optimizer = SGD(0.01),
                 batch_size=400,
                 max_epochs=50,
                 seed=42
                 ):

        self.network = network
        self.x_train = x_train
        self.t_train = t_train
        self.x_val = x_val
        self.t_val = t_val
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.train_loss_list = []
        self.train_acc_list = []
        self.test_acc_list = []
        self.random = np.random.RandomState(seed)

    def train(self):
        x_train = self.x_train
        t_train = self.t_train
        x_val = self.x_val
        t_val = self.t_val
        epoch_cnt = 0
        max_epochs = self.max_epochs
        train_size = self.x_train.shape[0]
        batch_size = self.batch_size
        optimizer = self.optimizer
        train_loss_list = self.train_loss_list
        train_acc_list = self.train_acc_list
        test_acc_list = self.test_acc_list
        iter_per_epoch = max(train_size / batch_size, 1)
        network = self.network

        for i in range(100000000):

            batch_mask = self.random.choice(train_size, batch_size)
            x_batch = x_train[batch_mask]
            t_batch = t_train[batch_mask]

            # 傾きを求める
            grads = network.gradient(x_batch, t_batch)

            # optimize
            optimizer.update(network.params, grads)

            train_loss_list.append(network.loss(x_batch, t_batch))
            print(f"loss:\t{train_loss_list[-1]}")

            if i != 0 and i % iter_per_epoch == 0:
                # train_acc_list.append(network.accuracy(x_batch, x_batch))
                # test_acc_list.append(network.accuracy(x_val, t_val))
                epoch_cnt += 1
                # print(f"epoch: {epoch_cnt}\ttrain_acc: {train_acc_list[-1]}\ttest_acc:{test_acc_list[-1]}")
                print(f"epoch: {epoch_cnt}")
                with open(f"network{epoch_cnt}.pkl", 'wb') as f:
                    pickle.dump(network, f)
                if epoch_cnt >= max_epochs:
                    break

    def show_graph(self, is_loss=True, is_accuracy=True):
        import matplotlib.pyplot as plt

        if is_loss:
            plt.plot(range(len(self.train_loss_list)), self.train_loss_list, label='loss')
            plt.xlabel("iteration")
            plt.ylabel("loss")
            plt.show()
        if is_accuracy:
            plt.plot(range(len(self.train_acc_list)), self.train_acc_list, label="train")
            plt.plot(range(len(self.test_acc_list)), self.test_acc_list, label="test")
            plt.xlabel("epochs")
            plt.ylabel("p")
            plt.ylim(ymax=1.0)
            plt.legend()
            plt.show()
