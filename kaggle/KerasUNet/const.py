import os

IMG_WIDTH=128
IMG_HEIGHT=128
IMG_CHANNELS=3
TRAIN_PATH = 'input/stage1_train/'
TEST_PATH = 'input/stage1_test/'
SEED = 42

train_ids = next(os.walk(TRAIN_PATH))[1]
test_ids = next(os.walk(TEST_PATH))[1]