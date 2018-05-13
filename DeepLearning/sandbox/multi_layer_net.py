from collections import OrderedDict
from multiprocessing import Pool
from typing import Tuple, List

import numpy as np

from sandbox.layers import ReLu, Affine, SoftmaxWithLoss, DropOut


class MultiLayerNet:

    def __init__(self, input_size: int,
                 hidden_layer_list: List[int],
                 output_size: int,
                 weight_init_std='he',
                 weight_decay_lambda=0.0,
                 use_drop_out = True,
                 drop_out_ratio = 0.15,
                 seed: int = 42):

        # 隠れ層
        self.weight_decay_lambda = weight_decay_lambda
        self.hidden_layer_list = hidden_layer_list

        # 重みの初期化: Wは最後にwight_initをかける
        self.params = {}
        r = np.random.RandomState(seed)
        # input_size => hidden_size
        self.params['W1'] = r.randn(input_size, hidden_layer_list[0])
        # hiddenのbias
        self.params['b1'] = np.zeros(hidden_layer_list[0])

        for i in range(len(hidden_layer_list) - 1):
            self.params[f'W{i+2}'] = r.randn(hidden_layer_list[i], hidden_layer_list[i + 1])
            self.params[f'b{i+2}'] = np.zeros(hidden_layer_list[i + 1])

        # hidden_size => output_size
        self.params[f'W{len(hidden_layer_list)+1}'] = \
            r.randn(hidden_layer_list[-1], output_size)

        # outputのbias
        self.params[f'b{len(hidden_layer_list)+1}'] = np.zeros(output_size)

        # Wの初期化
        if weight_init_std == 'he':
            for i in range(1, len(hidden_layer_list) + 2):
                self.params[f'W{i}'] = self.params[f'W{i}'] * np.sqrt(2 / self.params[f'W{i}'].shape[0])

        # レイヤの生成
        self.layers = OrderedDict()
        for i in range(1, len(hidden_layer_list) + 1):
            self.layers[f'Affine{i}'] = Affine(self.params[f'W{i}'], self.params[f'b{i}'])
            self.layers[f'Relu{i}'] = ReLu()
            if use_drop_out:
                self.layers[f'DropOut{i}'] = DropOut(dropout_raito=drop_out_ratio)

        self.layers[f'Affine{len(hidden_layer_list)+1}'] \
            = Affine(self.params[f'W{len(hidden_layer_list)+1}'],
                     self.params[f'b{len(hidden_layer_list)+1}'])
        self.last_layer = SoftmaxWithLoss()

    def predict(self, x: np.ndarray):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x

    def loss(self, x: np.ndarray, t: np.ndarray):
        """
        objectのLastLayer（Softmax層）を更新。戻値は表示用。
        :param x:
        :param t:
        :return:
        """

        # last_layer前まで前向きに更新
        pred_y = self.predict(x)

        weight_decay = 0
        for idx in range(1, len(self.hidden_layer_list) + 2):
            W = self.params[f'W{idx}']
            weight_decay += 0.5 * self.weight_decay_lambda * np.sum(W ** 2)

        # last_layerを更新 => 戻り値は使わない
        return self.last_layer.forward(pred_y, t) + weight_decay

    def accuracy(self, x: np.ndarray, t: np.ndarray):
        pred_y = self.predict(x)
        y = np.argmax(pred_y, axis=1)
        if t.ndim != 1:
            # one-hot vectorの場合
            np.argmax(t, axis=1)
        accuracy = np.sum(y == t) / x.shape[0]
        return accuracy

    def gradient(self, x, t):
        # forward
        self.loss(x, t)

        # backward
        dout = 1
        dout = self.last_layer.backward(dout)

        layers = list(self.layers.items())
        layers.reverse()
        for k, layer in layers:
            dout = layer.backward(dout)

        grads = {}
        for i in range(1, len(self.hidden_layer_list) + 2):
            grads[f'W{i}'] = self.layers[f'Affine{i}'].dW + \
                             self.weight_decay_lambda * self.layers[f'Affine{i}'].W
            grads[f'b{i}'] = self.layers[f'Affine{i}'].db

        return grads

    def numerical_gradient(self, x: np.ndarray, t: np.ndarray):
        # lossの関数 => Wによらず、xとtから求める
        loss_W = lambda W: self.loss(x, t)

        grads = {}
        for i in range(1, len(self.hidden_layer_list) + 2):
            grads[f'W{i}'] = self.layers[loss_W, self.params[f'W{i}']]
            grads[f'b{i}'] = self.layers[loss_W, self.params[f'b{i}']]

        return grads


# ここからテスト用

def test_nmst_init_weight(multi_layer_net: MultiLayerNet):
    from dataset.mnist import load_mnist
    (x_train, t_train), (x_test, t_test) = load_mnist(one_hot_label=True)
    network = multi_layer_net
    loss_hist = []
    iters_num = 2000
    train_size = x_train.shape[0]
    batch_size = 1000
    iter_per_epoch = max(train_size / batch_size, 1)
    learning_rate = 0.1
    print("train start")

    for i in range(iters_num):

        # ミニバッチの取得
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        # 勾配を計算
        grad = network.gradient(x_batch, t_batch)

        # パラメータの更新

        for key in (network.params.keys()):
            network.params[key] -= learning_rate * grad[key]

        # 誤差の記録
        loss = network.loss(x_batch, t_batch)
        loss_hist.append(loss)

        # if i % iter_per_epoch == 0:
        #     print(network.accuracy(x_test, t_test))
        #     train_acc = network.accuracy(x_train, t_train)
        #     test_acc = network.accuracy(x_test, t_test)
        #     train_acc_hist.append(train_acc)
        #     test_acc_hist.append(test_acc)
        #     print(f"{i}\ttrain_accuracy:{train_acc_hist[-1]}\ttest_accuracy:{test_acc_hist[-1]}")
    return loss_hist


def wrap_test_nmst_init_weight(args: Tuple[str, MultiLayerNet]):
    print(args[0])
    print(args[1])
    return args[0], test_nmst_init_weight(args[1])


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    nets = {"He": MultiLayerNet(784, [100, 100], 10, weight_init_std=np.sqrt(2 / 784)),
            "std=0.01": MultiLayerNet(784, [100, 100], 10, weight_init_std=np.sqrt(2 / 0.01)),
            "Xavier": MultiLayerNet(784, [100, 100], 10, weight_init_std=np.sqrt(1 / 784)), }

    p = Pool(processes=3)
    items = [(k, n) for k, n in nets.items()]
    print(items)
    results = p.map(wrap_test_nmst_init_weight, items)

    hists = {}
    for r in results:
        hists[r[0]] = r[1]

    for k, v in hists.items():
        plt.plot(range(len(v)), v, label=f"{k}")

    plt.legend()
    plt.show()

    # plt.plot(range(len(train_acc_hist)), train_acc_hist)
    # plt.plot(range(len(test_acc_hist)), test_acc_hist)
    # plt.show()
