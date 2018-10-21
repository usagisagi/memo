import os
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from tqdm import tqdm

from const import TRAIN_PATH, TEST_PATH, IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS, train_ids, test_ids

def load():
    # iterator
    X_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
    Y_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
    print('Getting and resizing train images and masks ...')
    sys.stdout.flush()

    for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):
        path = TRAIN_PATH + id_
        img = imread(path + '/images/' + id_ + '.png')[:, :, :IMG_CHANNELS]
        img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
        X_train[n] = img

        # 複数のmask画像を合成
        mask = np.zeros((IMG_HEIGHT, IMG_WIDTH, 1), dtype=bool)
        for mask_file in next(os.walk(path + '/masks'))[2]:
            mask_ = imread(path + '/masks/' + mask_file)
            mask_ = resize(mask_, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
            mask_ = np.expand_dims(mask_, axis=-1)
            mask = np.maximum(mask, mask_)
        Y_train[n] = mask

    X_test = np.zeros((len(test_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint)
    sizes_test = [] # testの元サイズを保持する
    print('Getting and resizing test images ...')
    sys.stdout.flush()

    for n, id_ in tqdm(enumerate(test_ids), total=len(test_ids)):
        path = TEST_PATH + id_
        img = imread(path + '/images/' + id_ + '.png')[:, :, :IMG_CHANNELS]
        sizes_test.append([img.shape[0], img.shape[1]])
        img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
        X_test[n] = img

    print('Done!')

    return X_train, Y_train, X_test, sizes_test


if __name__ == '__main__':
    _, Y_train, _, _ = load()
    num_train_ids = len(Y_train)
    ix = random.randint(0, num_train_ids)
    plt.imshow(np.squeeze(Y_train[ix]))
    plt.show()
