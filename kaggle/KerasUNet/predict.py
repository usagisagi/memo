import random

import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from skimage.transform import resize
from skimage.morphology import label
import load_img_data
from const import test_ids
from mean_iou import mean_iou
import pandas as pd

model = load_model('model-bsbowl1018-1.h5', custom_objects={'mean_iou': mean_iou})
X_train, Y_train, X_test, sizes_test = load_img_data.load()

n_validate = int(X_train.shape[0] * 0.9)
preds_train = model.predict(X_train[:n_validate], verbose=1)
preds_val = model.predict(X_train[n_validate:], verbose=1)
preds_test = model.predict(X_test, verbose=1)

preds_train_t = (preds_train > 0.5).astype(np.uint8)
preds_val_t = (preds_val > 0.5).astype(np.uint8)
preds_test_t = (preds_test > 0.5).astype(np.uint8)

preds_test_upsampled = []

for i in range(len(X_test)):
    resized_image = resize(np.squeeze(preds_test[i]),
                           (sizes_test[i][0], sizes_test[i][1]),
                           mode='constant',
                           preserve_range=True)
    preds_test_upsampled.append(resized_image)


def show_train_data():
    ix = random.randint(0, len(preds_train_t))
    plt.imshow(X_train[ix])
    plt.show()

    plt.imshow(np.squeeze(Y_train[ix]))
    plt.show()

    plt.imshow(np.squeeze(preds_train_t[ix]))
    plt.show()


def rle_encoding(x):
    # .T sets Fortran order down-then-right
    dots = np.where(x.T.flatten() == 1)[0]  # np.where(x.T.flatten() == 1)はindexを返す　
    run_lengths = []
    prev = -2

    for b in dots:  # 全部の1のindexに対して
        if b > prev + 1:  # 前と2以上離れていた時
            run_lengths.extend((b + 1, 0))  # b+1はスタートのindex

        run_lengths[-1] += 1
        prev = b
    return run_lengths


def prob_to_rles(x, cutoff=0.5):
    lab_img = label(x > cutoff)
    for i in range(1, lab_img.max() + 1):
        yield rle_encoding(lab_img == 1)


if __name__ == '__main__':
    new_test_ids = []
    rles = []
    for n, id_ in enumerate(test_ids):
        rle = list(prob_to_rles(preds_test_upsampled[n]))
        rles.extend(rle)
        new_test_ids.extend([id_] * len(rle))

    sub = pd.DataFrame()
    sub['ImageId'] = new_test_ids
    sub['EncodedPixels'] = pd.Series(rles).apply(lambda x: ' '.join(str(y) for y in x))
    sub.to_csv('sub-dsbowl2018-1.csv')
