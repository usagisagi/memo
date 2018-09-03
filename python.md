# Python #

## from inpynb to html ##

ipython nbconvert --to html {filename}

## 親フォルダ ##

```python
os.path.abspath(os.pardir + "\\data\\raw\\users.tsv")
```

## シングルトン ##

```python
class SimpleSingleton:
    _instance = None
    _lock = threading.Lock()

    # initの前に始めの1回呼ばれる
    def __new__(cls):
        with cls._lock:
            # 保持しているインスタンスが無かったら作成
            if cls._instance is None:
                cls._instance = Instance

        return cls._instance
```

## 日付 ##

```python
from datetime import datetime
import date

tstr = '2012-12-29 13:49:37'
tdatetime = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')

tstr = '2012-12-29 13:49:37'
tdatetime = datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)

tdatetime = dt.now()
tstr = tdatetime.strftime('%Y/%m/%d')
```

## pandas ##

### DataFrameのselect ###

filter => dropna

### ソート ###
> https://note.nkmk.me/python-pandas-sort-values-sort-index/

### CSV周り ###
> https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html

### 型変換 ###

```python

df['innings'] = df['innings'].fillna("-1.0")
df['innings'] = df['innings'].astype(np.int64)

```

### timedelta => hours ###

```python
td / np.timedelta64(1, 'h')
```

> https://stackoverflow.com/questions/31283001/get-total-number-of-hours-from-a-pandas-timedelta

### 値の更新 ###

```python
# チケットの料金を分類するため、'FareCteg'項目を追加
df_train['FareCateg'] = "0: <10"

# パラメータの第１引数に条件を指定して一致する場合に、第２引数で示した'Farecteg'に値を設定する
df_train.loc[df_train['Fare'].values >= 10, 'FareCateg'] = "1: 10<20"
df_train.loc[df_train['Fare'].values >= 20, 'FareCateg'] = "2: 20<30"
df_train.loc[df_train['Fare'].values >= 30, 'FareCateg'] = "3: 30+"
```

### pandasの関数適用 ###

+ 要素（スカラー値）に対する関数
    + Seriesの各要素に適用: map()
    + DataFrameの各要素に適用: applymap()
+ 行・列（一次元配列）に対する関数
    + DataFrame, Seriesの各行・各列に適用: apply()


### ndarrayのSeriesを新しい軸で積み重ねる ###

`np.stack(image_array_set)`

## Numpy ##

### one-hot-vector ###

```python
a_one_hot = np.identity(10)[a]
```

### concatnate ###

```python
a
Out[21]: 
array([[1, 2],
       [3, 4]])
b = np.array([[5,6],[7,8]])
b
Out[23]: 
array([[5, 6],
       [7, 8]])
np.concatenate((a, b), axis=0)
Out[24]: 
array([[1, 2],
       [3, 4],
       [5, 6],
       [7, 8]])
np.concatenate((a, b), axis=1)
Out[25]: 
array([[1, 2, 5, 6],
       [3, 4, 7, 8]])
```

### 配列の複製 ###
 
`np.tile`を用いる

```python
g = np.arange(9).reshape(3,3)
np.tile(g, 3)
# g.shape = (3,3,3)
```

### 画像処理 ###

関数は`tf.image`or`tf.keras`

方法はチュートリアルが詳しい
> https://www.tensorflow.org/api_guides/python/image#Converting_Between_Colorspaces

### 画像読み込み ###

```python
with open(file_path, 'rb') as f:
    img = tf.image.decode_image(f.read(), channels=3)   # discard alpha channel
    img = tf.reshape(img, img.eval().shape) # inputed 0-D Tensor, so need to resize
        
```

### ビット配列から整数に変換 ###

```python
b.dot(2**np.arange(b.size)[::-1])
```

## PyCharm開始スクリプト ##

```python
import sys;import os
print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend([WORKING_DIR_AND_PYTHON_PATHS])
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print("now_dir ->" + os.getcwd())
```

## from PIL import IMAGE でエラー ##

conda-forgeのpillowを使う


## 1日ごとのtimestampを作成する ##

```python
datelist = [fromday + datetime.timedelta(days=n) for n in range((today - fromday).days)]
```

## 文字列で"\u0000"とか来た時の対処法 ##

\\\\uでsplit => int(x,16)で変換 => chrで文字 => joinで接続

```python
''.join([chr(int(x, 16)) for x in tar.split("\\u")[1::]])
```

## 画像イメージをnumpyに変換 ##

np.array()にPIL.Image.open()で読み込んだ画像データを渡すとndarrayが得られる。

RGB画像は行（高さ） x 列（幅） x 色（3）の三次元のndarray、白黒画像は行（高さ） x 列（幅）の二次元のndarrayになる。

```python
from PIL import Image
import numpy as np

im = np.array(Image.open('data/src/lena_square.png'))

print(im.dtype)  # データ型
# uint8

print(im.ndim)  # 次元数
# 3

print(im.shape)  # サイズ（高さ x 幅 x 色数）
# (512, 512, 3)
```

> https://note.nkmk.me/python-numpy-image-processing/

## pytorch ##

### TensorBoardForPyTorch ###

conda
```python
conda install -c conda-forge tensorboardx
```

git
> https://github.com/lanpa/tensorboard-pytorch

可視化はtensorBoardで`-logdir = {runs}`

### graph可視化 ###

```python
from tensorboardX import SummaryWriter
dummy_input = Variable(torch.rand(13, 1, 28, 28))
with SummaryWriter(comment='densenet121') as w:
    model = torchvision.models.densenet121()    # modelはinstance
    w.add_graph(model, (dummy_input,))
```

## tensorflow ##

### modelのレストア ###

```python
init = tf.global_variables_initializer()
restore_saver = tf.train.import_meta_graph(model_name + ".meta")
with tf.Session() as sess:
    init.run()
    restore_saver.restore(sess, model_name)
```

### kernel初期化 ###

`tf.keras.initializers.{operation}`

heの初期化とかもできる。一様分布が標準らしいね。

### 精度の測定 ###

```python
with tf.name_scope('eval'):
    correct = tf.nn.in_top_k(logit, y, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name='accuracy')
```

### DL性能改善 ###
> https://qiita.com/jiny2001/items/d9dec2597648812ab8e5

### EarlyStopping ###

lossの最小のモデルを利用する

```python
# early_stopping用
best_loss_val = np.infty
check_interval = 50
checks_since_last_progress = 0
max_checks_without_progress = 50
best_model_params= None

# 学習フェーズ
with tf.Session() as sess:
    init.run()
    restore_saver.restore(sess, load_path)
    h5_cache = sess.run(hidden5, feed_dict={x: train_x})
    validate_dict = {x: validate_x, y: validate_y}
    test_dict = {x: test_x, y: test_y}

    for epoch in range(n_epochs):
        shuffled_idx = np.random.permutation(train_x.shape[0])
        hidden5_batches = np.array_split(h5_cache[shuffled_idx], n_batches)
        y_batches = np.array_split(train_y[shuffled_idx], n_batches)
        for idx, (hidden5_batch, y_batch) in enumerate(zip(hidden5_batches, y_batches)):
            sess.run(training_op, feed_dict={hidden5: hidden5_batch, y: y_batch})

            if is_early_stop:
                if idx % check_interval == 0:
                    loss_val = loss.eval(feed_dict=validate_dict)
                    if loss_val < best_loss_val:
                        best_loss_val = loss_val
                        checks_since_last_progress = 0
                        best_model_params = get_model_params()
                    else:
                        checks_since_last_progress += 1

            writer.add_summary(loss_summary.eval(feed_dict=validate_dict), epoch * n_batches + idx)
        print(epoch, ' epoch accuracy:', accuracy.eval(feed_dict=validate_dict))
        print('best loss:', best_loss_val)
        if checks_since_last_progress > max_checks_without_progress:
            print('early stopping')
            break

    if best_model_params:
        restore_model_params(best_model_params)
    print('test data accuracy:', accuracy.eval(feed_dict=test_dict))
    saver.save(sess, save_path)
```

### kerasの画像前処理 ###

`tf.keras.preprossing`を用いる

コンストラクタで処理方法を規定し、flowでbatchを生成

> https://keras.io/ja/preprocessing/image/
> https://keras.io/preprocessing/image/

.flowで投入

+ random_crop => `tf.random_crop`がある

前処理の説明
> http://aidiary.hatenablog.com/entry/20161212/1481549365


### TFRecord ###

#### 最終解 ####

> https://stackoverflow.com/questions/45427637/numpy-to-tfrecords-is-there-a-more-simple-way-to-handle-batch-inputs-from-tfrec/45428167

```python
def npy_to_tfrecords(...):
    # write records to a tfrecords file
    writer = tf.python_io.TFRecordWriter(output_file)

    # Loop through all the features you want to write
    for ... :
        # let say X is of np.array([[...][...]])
        # let say y is of np.array[[0/1]]

        # Feature contains a map of string to feature proto objects
        feature = {}
        feature['X'] = tf.train.Feature(float_list=tf.train.FloatList(value=X.flatten()))
        feature['y'] = tf.train.Feature(int64_list=tf.train.Int64List(value=y))

        # Construct the Example proto object
        example = tf.train.Example(features=tf.train.Features(feature=feature))

        # Serialize the example to a string
        serialized = example.SerializeToString()

        # write the serialized objec to the disk
        writer.write(serialized)
    writer.close()

# Creates a dataset that reads all of the examples from filenames.
filenames = ["file1.tfrecord", "file2.tfrecord", ..."fileN.tfrecord"]
dataset = tf.contrib.data.TFRecordDataset(filenames)

# for version 1.5 and above use tf.data.TFRecordDataset

# example proto decode

def _parse_function(example_proto):
    keys_to_features = {'X':tf.FixedLenFeature((shape_of_npy_array), tf.float32),
                        'y': tf.FixedLenFeature((), tf.int64, default_value=0)}
    parsed_features = tf.parse_single_example(example_proto, keys_to_features)
    return parsed_features['X'], parsed_features['y']

# Parse the record into tensors.
dataset = dataset.map(_parse_function)  

# Shuffle the dataset
dataset = dataset.shuffle(buffer_size=10000)

# Repeat the input indefinitly
dataset = dataset.repeat()  

# Generate batches
dataset = dataset.batch(batch_size)

# Create a one-shot iterator
iterator = dataset.make_one_shot_iterator()

# Get batch X and y
X, y = iterator.get_next()
```

#### memo ####
やっぱり固めた段階でTensorにするしかない

class TFRecordは入出力がTensorのみっぽいので注意
mapを使ってparseするのは`Parsing tf.Example protocol buffer messages`、`Decoding image data and resizing it`に記載
（最も、Tensorまで落とし込んで初めて**前処理ができた**なのだけど）
> https://www.tensorflow.org/guide/datasets

DataSetsのAPIはここ
> https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#shuffle

Imageのパースとreshapeはここ利用
> http://warmspringwinds.github.io/tensorflow/tf-slim/2016/12/21/tfrecords-guide/


ここたへんは低水準でわかりやすいかも
> https://www.tensorflow.org/api_guides/python/reading_data#_QueueRunner_

後半でバッチ処理について解説

> https://qiita.com/YusukeSuzuki@github/items/1388534bc274bc64b9b2#%E5%8F%82%E8%80%83--%E8%87%AA%E5%89%8D%E3%81%AE%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E5%BD%A2%E5%BC%8F%E3%81%A8%E8%87%AA%E5%89%8D%E3%81%AE%E9%9D%9E%E5%90%8C%E6%9C%9F%E8%AA%AD%E3%81%BF%E8%BE%BC%E3%81%BF%E3%81%AE%E3%82%B3%E3%83%BC%E3%83%89

前処理関連
> https://www.tensorflow.org/performance/datasets_performance

一番わかり易い
> https://qiita.com/antimon2/items/c7d2285d34728557e81d
> https://www.cresco.co.jp/blog/entry/3024/

#### padded_batch ####

padded_shapeはtupleにする
datasetを返すので注意
```python

dataset.padded_batch(batch_size, padded_shapes=([800, 600, 3],[800, 600, 3],[800, 600, 4]))
```

> https://stackoverflow.com/questions/45955241/how-do-i-create-padded-batches-in-tensorflow-for-tf-train-sequenceexample-data-u

### GPUのメモリ関連 ###

session毎にメモリの最大値を制限する

```python
config = tf.ConfigProto(
    gpu_options=tf.GPUOptions(
        per_process_gpu_memory_fraction=0.5 # 最大値の50%まで
    )
)
sess = sess = tf.Session(config=config)
```

他の方法もある
> https://qiita.com/kikusumk3/items/907565559739376076b9

### FCN 実装例 ###
。https://qiita.com/tktktks10/items/0f551aea27d2f62ef708

### name scopeの取得法 ###

`tf.contrib.framework.get_name_scope`

> https://stackoverflow.com/questions/40907769/how-to-get-current-tensorflow-name-scope

## sklearn ##

### 自作Estimator ###

使い方はpythonで始める機械学習が一番くわしい

公式

> http://scikit-learn.org/stable/developers/contributing.html#rolling-your-own-estimator

多分get_paramとset_paramはいらない

> https://qiita.com/_takoika/items/89a7e42dd0dc964d0e29

あたらしいけど真似しないほうが

> https://qiita.com/roronya/items/fdf35d4f69ea62e1dd91#%E4%BE%8B1-%E8%87%AA%E4%BD%9Clinearregression

### train-test-validation ###

```python
X_train, X_test, y_train, y_test 
    = train_test_split(X, y, test_size=0.2, random_state=1)

X_train, X_val, y_train, y_val 
    = train_test_split(X_train, y_train, test_size=0.2, random_state=1)
```

### 標準分布へ正規化 ###

StandardScaler

## PIL ##

HandBook/Tutorialに色々ある

> https://pillow.readthedocs.io/en/5.2.x/index.html

## Pandas From MySQL ##

> https://qiita.com/takahashi_yukou/items/10f1510c7b433e114e70
