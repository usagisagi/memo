from typing import Tuple

import tensorflow as tf
from tensorflow import TensorShape, Tensor

import numpy as np


def pooling(input: Tensor,
            ksize,
            strides,
            padding: str = 'VALID',
            name: str = 'pooling') -> Tuple[Tensor, Tensor, TensorShape]:
    """
    pooling層。実質pooling_with_arg_max。

    :param input:
    :param ksize:
    :param strides:
    :param padding:
    :param name:
    :return:
        次ノードへのTensor, argmaxのインデックス位置、inputのshape
    """
    with tf.name_scope(name):
        input_shape = input.get_shape()
        output, argmax = \
            tf.nn.max_pool_with_argmax(input, ksize, strides, padding)
        return output, argmax, input_shape


def unpooling(input: Tensor,
              argmax: Tensor,
              output_shape: TensorShape,
              name='unpooling'):
    """
    unpooling層

    :param input:
    :param argmax:
    :param output_shape:
    :return:
        次ノードへのTensor
    """

    with tf.name_scope(name):
        # inputを直線に並べる
        input_stride = tf.reshape(input, [-1])

        # argmaxを直線に並べる。1行1要素の2次元になる。
        argmax_stride = tf.reshape(argmax, [-1, 1])

        # outputの要素数
        num_elem = output_shape.num_elements()

        # inputをargmaxに従い、num_elemの1行Tensorに再配置
        output_stride = tf.scatter_nd(argmax_stride, input_stride, [num_elem])

        output = tf.reshape(output_stride, output_shape)

        return output


if __name__ == '__main__':
    input = tf.constant(np.arange(16).reshape(1, 4, 4, 1))
    init = tf.global_variables_initializer()
    pooled, argmax, shape = pooling(input, [1, 2, 2, 1], [1, 2, 2, 1])
    unpooled = unpooling(pooled, argmax, shape)
    unpooled_view = tf.reshape(unpooled, (4, 4))

    writer = tf.summary.FileWriter("./logdir/", tf.get_default_graph())
    with tf.Session() as sess:
        init.run()
        print(unpooled_view.eval())

    writer.close()