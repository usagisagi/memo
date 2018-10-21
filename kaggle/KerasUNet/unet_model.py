import random
import warnings

import numpy as np

from keras.layers import Input
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.core import Dropout, Lambda
from keras.layers.merge import concatenate
from keras.layers.pooling import MaxPooling2D
from keras.models import Model

from const import IMG_CHANNELS, IMG_HEIGHT, IMG_WIDTH, SEED
from mean_iou import mean_iou

warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
random.seed = SEED
np.random.seed = SEED


def build_Unet_model():
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))

    def conv_twice(init_tensor, n_filters, drop_rate):
        c = Conv2D(n_filters, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(init_tensor)
        c = Dropout(drop_rate)(c)
        c = Conv2D(n_filters, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c)
        return c

    def conv_pooling(init_tensor, n_filters, drop_rate):
        """conv => drop => conv => maxpooling"""
        c = conv_twice(init_tensor, n_filters, drop_rate)
        p = MaxPooling2D((2, 2))(c)
        return c, p

    def convtrans_conv(init_tensor, n_filters, drop_rate, conctatenate_tensor, is_concat_axis3=False):
        u = Conv2DTranspose(n_filters, (2, 2), strides=(2, 2), padding='same')(init_tensor)
        u = concatenate([u, conctatenate_tensor], axis=3 if is_concat_axis3 else -1)
        c = conv_twice(u, n_filters, drop_rate)
        return c

    s = Lambda(lambda x: x / 255)(inputs)
    c1, p1 = conv_pooling(s, n_filters=16, drop_rate=0.1)
    c2, p2 = conv_pooling(p1, n_filters=32, drop_rate=0.1)
    c3, p3 = conv_pooling(p2, n_filters=64, drop_rate=0.2)
    c4, p4 = conv_pooling(p3, n_filters=128, drop_rate=0.2)
    c5 = conv_twice(p4, n_filters=256, drop_rate=0.3)
    c6 = convtrans_conv(c5, n_filters=128, drop_rate=0.2, conctatenate_tensor=c4)
    c7 = convtrans_conv(c6, n_filters=64, drop_rate=0.2, conctatenate_tensor=c3)
    c8 = convtrans_conv(c7, n_filters=32, drop_rate=0.1, conctatenate_tensor=c2)
    c9 = convtrans_conv(c8, n_filters=16, drop_rate=0.1, conctatenate_tensor=c1, is_concat_axis3=True)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(c9)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[mean_iou])
    return model


if __name__ == '__main__':
    model = build_Unet_model()
    model.summary()
