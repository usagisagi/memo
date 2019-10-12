# Kotlin #

## IntelliJにGrandleインストール, Jar生成まで #

> http://biacco42.hatenablog.com/entry/2017/05/24/202849


## Grandle Projectを自動生成して Rest APIを作って見たもの ##

> https://qiita.com/yusuke_dev/items/79c980ff7002d68f9aa5

## 基本型の配列 ##

`List<{type}>`ではなく`{type}Array`を使う

> https://qiita.com/KenjiOtsuka/items/e3d42f34ee731747220d

### 多次元配列 ###

```kotlin
Array(size: Int, init: (Int) -> T)

Array(10, { index ->
    index // 0から9が順々に
})

// もちろんitで参照できる
Array(10, {it})

// 要素を全て２で初期化する例
Array(10, {index ->
    2
})

// 上はindexを使ってないので省略する
Array(10, {2}})
```

> https://qiita.com/yasukotelin/items/1750b8f17b2c17233cd9
