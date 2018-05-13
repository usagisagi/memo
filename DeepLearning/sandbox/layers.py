import numpy as np

from func import sigmoid, softmax, cross_entropy_error, col2im, im2col


class MulLayer:
    def __init__(self):
        self.x = None
        self.y = None

    def forward(self, x, y):
        self.x = x
        self.y = y
        return x * y

    def backward(self, dout):
        dx = self.y * dout
        dy = self.x * dout
        return dx, dy


class AddLayer:
    def __init__(self):
        pass

    def forward(self, x, y):
        return x + y

    def backward(self, dout):
        # dx, dy
        return dout, dout


class ReLu:
    def __init__(self):
        self.mask = None

    def forward(self, x: np.array):
        self.mask = (x <= 0)
        out = x.copy()  # outを変えてもxを変えないため
        out[self.mask] = 0  # コピーせずに元をxにすると元のxまで変わってしまう(numpyはmutable)
        return out

    def backward(self, dout: np.array):  # backwardの時、doutは1回しか使わない
        dout[self.mask] = 0
        dx = dout
        return dx


class Sigmoid:
    def __init__(self):
        self.out: np.array = None

    def forward(self, x: np.array):
        out = sigmoid(x)
        self.out = out
        return out

    def backward(self, dout: np.array):
        dx = dout * (1.0 - self.out) * self.out
        return dx


class Affine:
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.x = None
        self.original_x_shape = None
        self.dW = None
        self.db = None

    def forward(self, x: np.array):
        self.original_x_shape = x.shape
        # 2次元にする(N, C*W*H)
        x = x.reshape(x.shape[0], -1)
        self.x = x
        return np.dot(self.x, self.W) + self.b

    def backward(self, dout: np.array):
        self.dW = np.dot(self.x.T, dout)
        self.db = np.sum(dout, axis=0)
        dx = np.dot(dout, self.W.T)

        # 元の形状に戻す
        dx = dx.reshape(self.original_x_shape)
        return dx


class SoftmaxWithLoss:
    def __init__(self):
        self.loss = None
        self.y = None
        self.t = None

    def forward(self, x: np.array, t: np.array):
        self.t = t
        self.y = softmax(x)
        self.loss = cross_entropy_error(self.y, self.t)
        return self.loss

    def backward(self, dout=1):
        batch_size = self.t.shape[0]
        if self.t.size == self.y.size:
            dx = (self.y - self.t) / batch_size
        else:
            dx = self.y.copy()
            dx[np.arange(batch_size), self.t] -= 1
            dx = dx / batch_size

        return dx


class DropOut:
    def __init__(self, dropout_raito=0.5):
        self.dropout_raito = dropout_raito
        self.mask = None

    def forward(self, x, train_flg=True):
        if train_flg:
            self.mask = np.random.rand(*x.shape) > self.dropout_raito
            return x * self.mask
        else:
            return x * (1.0 - self.dropout_raito)

    def backward(self, dout):
        return dout * self.mask


class Convolution:

    def __init__(self, W, b, stride=1, pad=0):
        """

        :param W: (FN, C, FH, FW)
        :param b: ()
        :param stride:
        :param pad:
        """
        self.W = W
        self.b = b
        self.stride = stride
        self.pad = pad

        self.x = None
        self.col = None
        self.col_W = None

    def forward(self, x):
        # FH x FW => フィルター
        # Wは4次元
        FN, C, FH, FW = self.W.shape
        N, C, H, W = x.shape
        out_h = int(1 + (H + 2 * self.pad - FH) / self.stride)
        out_w = int(1 + (W + 2 * self.pad - FW) / self.stride)

        # x => (N * out_h * out_w, C * FH * FW）
        col = im2col(x, FH, FW, stride=self.stride, pad=self.pad)

        # フィルターの展開
        # (C * FH * FW, FN)
        col_W = self.W.reshape(FN, -1).T

        # (N * out_h * out_w, FN)
        out = np.dot(col, col_W) + self.b  # フィルターの内積

        # (N, out_h, out_w, FN) => (N, FN, out_h, out_w)
        out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)

        self.x = x
        # 展開後 x
        self.col = col
        # 展開後 W
        self.col_W = col_W

        return out

    def backward(self, dout: np.array):
        FN, C, FH, FW = self.W.shape

        # dout展開
        # (N, FN, out_h, out_w)
        # => (N, out_h, out_w, FN)
        # => (N * out_h * out_w, FN)
        dout = dout.transpose(0, 2, 3, 1).reshape(-1, FN)

        # dout -> db
        # doutの和をとってdbへ押し込む
        # (N, FN, out_h, out_w) -> (FN, out_h, out_w)
        self.db = np.sum(dout, axis=0)

        # dout -> W方向
        # 展開後 x の転置 ・ 展開後dout
        # (FH * FW * C, N * out_h * out_w）・(N * out_h * out_w, FN)
        # => (FH * FW * C, FN)
        # あとでoptimizerに使う
        self.dW = np.dot(self.col.T, dout)

        # 畳み込み.　im2colではC=>y=>xで畳み込んだので
        # reshapeしてもとに戻すとC, FH, FWとなる
        self.dW = self.dW.transpose(1, 0).reshape(FN, C, FH, FW)

        # dout -> x方向
        # (N * out_h * out_w, FN)・(FN, C*FH*FW)
        # => (N * out_h * out_w, C * FH * FW)
        dcol = np.dot(dout, self.col_W.T)

        dx = col2im(dcol, self.x.shape, FH, FW, self.stride, self.pad)

        return dx

    @staticmethod
    def __test():
        W = np.random.rand(10, 3, 4, 4)  # (FN, C, FH, FW)
        b = np.random.rand(5, 10, 6, 6)  # (N, FN, out_h, out_w)
        x = np.random.rand(5, 3, 7, 7)  # (N, C, y, x)
        stride = 1
        pad = 1

        # out_h = int(1 + (H + self.pad - FH) / self.stride)
        # out_w = int(1 + (W + self.pad - FW) / self.stride)
        convolution = Convolution(W, b, stride, pad)
        convolution.forward(x)

        # col: (180, 48)
        # col_W: (48, 10)
        # raw_out: (180, 10)
        # out: (5, 10, 6, 6)


class Pooling:
    def __init__(self, pool_h, pool_w, stride=1, pad=0):
        self.pool_h = pool_h
        self.pool_w = pool_w
        self.stride = stride
        self.pad = pad

        self.x = None
        self.arg_max = None

    def forward(self, x):
        N, C, H, W = x.shape
        out_h = int(1 + (H + 2 * self.pad - self.pool_h) / self.stride)
        out_w = int(1 + (W + 2 * self.pad - self.pool_w) / self.stride)

        # (N * out_h * out_y, C * pool_w * pool_h)
        col = im2col(x, self.pool_h, self.pool_w, self.stride, self.pad)

        col = col.reshape(-1, self.pool_h * self.pool_w)

        # maxの座標を記録する
        arg_max = np.argmax(col, axis=1)

        # (N * out_h * out_w * C, 1)
        out = np.max(col, axis=1)

        # (N, C, out_h, out_w)
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)

        self.x = x
        self.arg_max = arg_max

        return out

    def backward(self, dout):
        """
        (N, C, out_h, out_w) => (N, C, H, W)
        :param dout:
        """

        # (N, out_h, out_w, C)
        dout = dout.transpose(0, 2, 3, 1)

        pool_size = self.pool_w * self.pool_h

        # (N * out_h * out_w * C, pool_size)
        dmax = np.zeros((dout.size, pool_size))

        # dmaxの[]内:
        # 0次元: [0, 1, 2, 3, ...]
        # 1次元: [arg_max[0], arg_max[1], arg_max[2], ...]
        # 最大値だけ通す
        # flattenの意味は???
        dmax[np.arange(self.arg_max.size), self.arg_max.flatten()] = dout.flatten()

        # (N * out_h * out_w * C, pool_size) => (N, out_h, out_w, C, pool_size)
        dmax = dmax.reshape(dout.shape + (pool_size,))

        # (N * out_h * out_w, C * pool_w * pool_h)
        dcol = dmax.reshape(dmax.shape[0] * dmax.shape[1] * dmax.shape[2], -1)

        dx = col2im(dcol, self.x.shape, self.pool_h, self.pool_h, self.stride, self.pad)

        return dx
