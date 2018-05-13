from typing import Callable, Any

import numpy as np


def sigmoid(x):
    # http://www.kamishima.net/mlmpyja/lr/sigmoid.html#id11
    return 1 / (1 + np.exp(-x))


def identity_function(x):
    return x


def softmax(x: np.ndarray):
    if x.ndim == 2:
        # サンプルサイズが複数の時　shape(out, N)
        x = x.T  # shape(N, out)
        x = x - np.max(x, axis=0)
        y = np.exp(x) / np.sum(np.exp(x), axis=0)  # 和はサンプル毎に計算
        return y.T  # shape(out, N)

    x = x - np.max(x)  # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x))


def mean_squared_error(y, t):
    return 0.5 * np.sum((y - t) ** 2)


def cross_entropy_error(pred_y: np.ndarray, t: np.ndarray):
    """
    クロスエントロピーエラーを求める
     - 1/N Σ Σ  t_ij log(y_ij)

    :param pred_y: 予測値
    :param t: 正解ラベル
    :return: 誤差（スカラー）
    """
    if pred_y.ndim == 1:
        # データが1つの場合　=> 1次元でやってきた場合: 2次元(1, ndim)にreshape
        t = t.reshape(1, t.size)
        pred_y = pred_y.reshape(1, pred_y.size)

    # 教師データがone_hot_vectorの場合、tをindexに変換
    if pred_y.size == t.size:
        t = np.argmax(t, axis=1)

    batch_size = pred_y.shape[0]
    # pred_y[np.arange(batch_size), t] => pred_yの位置をnp.arange(何番目のサンプルか)とt(位置）で表現
    return -np.sum(np.log(pred_y[np.arange(batch_size), t] + 1e-7)) / batch_size


def numerical_diff(f, x):
    h = 1e-4
    return (f(x + h) - f(x - h)) / (2 * h)


def tangent_line(f, x):
    d = numerical_diff(f, x)
    y = f(x) - d * x
    return lambda t: d * t + y


def numerical_gradient(f: Callable[[np.ndarray], Any], x: np.ndarray) -> np.ndarray:
    """
    数値微分

    :param f: 微分対象関数(引数はnp.ndarrayの1つ)
    :param x: 微分の対象となる接点
    :return:  微分値
    """

    h = 1e-4
    grad = np.zeros_like(x)
    # multi_indexでindexにタプルを許可
    # readwriteで読み書きが可能になる
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])

    while not it.finished:  # indexの値を動かし、それ以外の値を固定する
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h  # f(x+h)
        fxh1 = f(x)

        x[idx] = float(tmp_val) - h  # f(x-h)
        fxh2 = f(x)

        grad[idx] = (fxh1 - fxh2) / (2 * h)

        x[idx] = tmp_val  # もとに戻す
        it.iternext()

    return grad


def gradient_descent(f: Callable, init_x: np.ndarray, lr: float = 0.01, step_num: int = 100) -> np.ndarray:
    """
    SGD

    :param f:　微分対象関数
    :param init_x: 初期値
    :param lr: 学習率
    :param step_num:　イテレーション数
    :return: 最適化されたx
    """
    x = init_x
    for i in range(step_num):
        if i % 10 == 0:
            grad = numerical_gradient(f, x)
        x -= lr * grad
    return x


def function_1(x):
    return 0.01 * x ** 2 + 0.1 * x


def function_2(x):
    return x[0] ** 2 + x[1] ** 2


def im2col(input_data, filter_h, filter_w, stride=1, pad=0):
    # N:個数
    # C:チャネル
    # H:高さ
    # W:幅
    N, C, H, W = input_data.shape

    # 出力行列の行列の数
    out_h, out_w = calc_out_hw(H, W, filter_h, filter_w, pad, stride)

    # HとWにpadding
    # (N, C, H + 2 * pad, W + 2 * pad)
    img = np.pad(input_data, [(0, 0), (0, 0), (pad, pad), (pad, pad)], 'constant')

    # 出力行列の枠
    col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

    # フィルタをずらしつつ展開する
    # フィルタ内の各位置ごとの処理
    # = x, yはフィルタのサイズだけloop
    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w
            # _maxはそのフィルタが及ぶ最大値
            # x、yはフィルターの位置

            # colに設定
            # 1つのフィルターの位置ごとに計算を行う
            # 1次元目:pad済みのImgのNをコピー
            # 2次元目:pad済みのImgのCをコピー
            # 3次元目:フィルタのy座標
            # 4次元目:フィルタのx座標
            # 5次元目:フィルタyが及ぶ範囲(strideごと)
            # 6次元目:フィルタxが及ぶ範囲(strideごと)
            # (*, *, y, x, *, *)は、フィルター(x, y)の(N,C,img_x,img_y)の4次元ブロック
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    # 6次元を2次元にする
    # 個数*xの範囲*yの範囲 => 1行
    # フィルタ縦 * フィルタ横 * チャネル => 1列
    # transpozeでは2次元展開するための区切りを決めている。
    # 個数、チャネル、yの範囲、xの範囲、y、x
    # => (N * out_h * out_w[前3つ],  C * フィルターy(FH) * フィルターx(FW)[後3つ]
    # 展開の順序は C=>y=>x
    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N * out_h * out_w, -1)
    return col


def col2im(dcol, input_shape, filter_h, filter_w, stride, pad):
    """
    backward時にdcol -> dxに基に戻す
    :param dcol:
    :param x_shape:
    :param FH:
    :param FW:
    :param stride:
    :param pad:
    :return:
    """

    N, C, H, W = input_shape
    # input_shapeを求める
    out_h, out_w = calc_out_hw(H, W, filter_h, filter_w, pad, stride)

    # (N * out_h * out_w[前3つ],  C * フィルターy(FH) * フィルターx(FW)[後3つ]
    # => 個数、チャネル、yの範囲、xの範囲、y、x
    col = dcol.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)

    # dxのimgの枠を生成
    img = np.zeros((N, C, H + 2 * pad, W + 2 * pad))

    # stride > 2の時 ???
    # ずれが生じた時のBuffer???
    # img = np.zeros((N, C, H + 2 * pad + stride - 1, W + 2 * pad + stride - 1))

    # colを生成した際のフィルターの位置(N, C, x, y)ごとに計算を行う
    # フィルターの位置座標毎に、その座標が通った画像の要素の群に、colの要素を足していく
    # （逆に写像する）
    # 重複も生じる
    for y in range(filter_h):
        y_max = y + stride * out_h
        for x in range(filter_w):
            x_max = x + stride * out_w

            # 1次元目:pad済みのImgのNをコピー
            # 2次元目:pad済みのImgのCをコピー
            # 3次元目4次元目col(x, y)時点を生成した時に参照していたimg中の座標
            # 展開時に生じた重複要素を吸収するため、和を取っていることに注意
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]

    # depadding
    # 画像が存在する部分をスライス
    return img[:, :, pad:H + pad, pad:W + pad]


def calc_out_hw(H, W, filter_h, filter_w, pad, stride):
    # 出力行列の行列の数
    out_h = (H + 2 * pad - filter_h) // stride + 1
    out_w = (W + 2 * pad - filter_w) // stride + 1
    return out_h, out_w


if __name__ == '__main__':
    import sys, os

    C = 3
    H = 7
    W = 7
    FH = 3
    FW = 3
    stride = 2
    pad = 1

    x1 = np.random.rand(1, C, H, W)
    col1 = im2col(x1, FH, FW, stride=stride, pad=pad)
    img = col2im(col1, x1.shape, FH, FW, stride, pad)
    print(col1.shape)
