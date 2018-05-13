from collections import OrderedDict
from typing import Dict
import numpy as np

from layers import Convolution, ReLu, Pooling, Affine, SoftmaxWithLoss


class SimpleConvNet:
    def __init__(self,
                 input_dim=(1, 28, 28),  # (C, W, H)
                 filter_num=30,
                 filter_size=5,
                 filter_pad=0,
                 filter_stride=1,
                 hidden_size=100,
                 output_size=10,
                 weight_init_std=0.01
                 ):
        # input(N, C, W, H)
        # -> Conv(N, FN, conv_out_h, conv_out_w) -> ReLu
        # -> Pooling(N, FN , pool_out_h, pool_out_w)
        # -> Affine[flatten行う](N, hidden_layer) -> ReLu
        # -> Affine(N, output_layer) -> SoftMax

        # input_sizeは動的に決定(正方形を前提)
        input_size = input_dim[1]
        conv_output_size = (input_size + 2 * filter_pad - filter_size) / filter_stride + 1
        # FN * pool_out_h * pool_out_w
        pool_output_size = int(filter_num * (conv_output_size / 2) * (conv_output_size / 2))

        self.params = {}

        # Conv
        # (input_size, C, W, H) -> (N, FilterNum, out_h, out_w)
        self.params['W1'] = \
            weight_init_std * np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params['b1'] = np.zeros(filter_num)

        # ReLu
        # Pool
        # Affine
        self.params['W2'] = weight_init_std * np.random.randn(pool_output_size, hidden_size)
        self.params['b2'] = np.zeros(hidden_size)

        # Relu
        # Affine
        self.params['W3'] = weight_init_std * np.random.randn(hidden_size, output_size)
        self.params['b3'] = np.zeros(output_size)

        self.layers = OrderedDict()

        self.layers['Conv1'] = Convolution(self.params['W1'], self.params['b1'], filter_stride, filter_pad)
        self.layers['ReLu1'] = ReLu()
        self.layers['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Affine1'] = Affine(self.params['W2'], self.params['b2'])
        self.layers['ReLu2'] = ReLu()
        self.layers['Affine2'] = Affine(self.params['W3'], self.params['b3'])

        self.last_layer = SoftmaxWithLoss()

    def predict(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x

    def loss(self, x, t):
        pred_y = self.predict(x)
        return self.last_layer.forward(pred_y, t)

    def gradient(self, x, t):
        self.loss(x, t)

        dout = 1
        dout = self.last_layer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()

        for layer in layers:
            dout = layer.backward(dout)

        grads = {
            'W1': self.layers['Conv1'].dW,
            'b1': self.layers['Conv1'].db,
            'W2': self.layers['Affine1'].dW,
            'b2': self.layers['Affine1'].db,
            'W3': self.layers['Affine2'].dW,
            'b3': self.layers['Affine2'].db
        }

        return grads

    def accuracy(self, x: np.ndarray, t: np.ndarray):
        pred_y = self.predict(x)
        y = np.argmax(pred_y, axis=1)
        if t.ndim != 1:
            # one-hot vectorの場合
            np.argmax(t, axis=1)
        accuracy = np.sum(y == t) / x.shape[0]
        return accuracy


if __name__ == '__main__':
    pass
