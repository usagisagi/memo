# Python #

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

## 画像イメージをnumpuyに変換 ##

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
    model = torchvision.models.densenet121()
    w.add_graph(model, (dummy_input,))
```

## tensorflow ##

### 保存済モデルからのVariable抽出 ###

```python
import Tensorflow as tf

# グラフ構造import
saver = tf.train.import_meta_graph('models/my_model_final.ckpt.meta')

# sessionにグラフ構造をrestore
sess = saver(sess, 'models/my_model_final.ckpt')

# variablesのリストを取得
tvars = tf.trainable_variables()

# variableの値を取得
tvars_vals = sess.run(tvars)
```

> https://github.com/google/prettytensor/issues/6

