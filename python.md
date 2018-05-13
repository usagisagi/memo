# Python #

## 親フォルダ ##

```python
os.path.abspath(os.pardir + "\\data\\raw\\users.tsv")
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