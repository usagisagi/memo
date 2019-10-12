# Kotlin #

## IntelliJにGrandleインストール, Jar生成まで #

> http://biacco42.hatenablog.com/entry/2017/05/24/202849


## Grandle Projectを自動生成して Rest APIを作って見たもの ##

> https://qiita.com/yusuke_dev/items/79c980ff7002d68f9aa5

## コレクション関連 ##

> https://qiita.com/opengl-8080/items/36351dca891b6d9c9687#to%E5%87%A6%E7%90%86%E7%B5%90%E6%9E%9C%E3%82%92%E6%9B%B8%E3%81%8D%E8%BE%BC%E3%81%BF%E5%8F%AF%E8%83%BD%E3%81%AA%E3%82%B3%E3%83%AC%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%81%AB%E8%BF%BD%E5%8A%A0%E3%81%99%E3%82%8B%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89

### 基本型の配列 ###

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
