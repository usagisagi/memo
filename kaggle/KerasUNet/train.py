"""https://www.kaggle.com/keegil/keras-u-net-starter-lb-0-277"""

from keras.callbacks import EarlyStopping, ModelCheckpoint

import load_img_data
import unet_model

X_train, Y_train, X_test = load_img_data.load()
early_stopper = EarlyStopping(patience=5, verbose=1)
checkpointer = ModelCheckpoint('model-bsbowl1018-1.h5', verbose=1, save_best_only=True)
model = unet_model.build_Unet_model()

result = model.fit(X_train, Y_train, validation_split=0.1, batch_size=16, epochs=50,
                   callbacks=[early_stopper, checkpointer])


if __name__ == '__main__':
    pass




