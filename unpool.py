import tensorflow as tf


def pooling(input,
            ksize=tf.constant([1, 2, 2, 1]),
            strides=tf.constant([1, 2, 2, 1]),
            padding='VALID',
            name='pooling'):
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
            tf.nn.max_pool_with_argmax(input, ksize, strides, padding, Targmax=tf.int32)
        return output, argmax, input_shape

def unpooling(input, argmax, output_shape, name):
    """
    unpooling層

    :param input:
    :param argmax:
    :param output_shape:
    :return:
        次ノードへのTensor
    """

    with tf.name_scope(name):
        # inputを1次元にする
        tf.reshape(input, [-1])
