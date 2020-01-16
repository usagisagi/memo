# Kotlin #

## build.gradleの構成 ##

```
plugins {
    id 'org.jetbrains.kotlin.jvm' version '1.3.61'
}

version '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}
test {
    useJUnitPlatform()
}

dependencies {
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jdk8"
    testImplementation 'io.kotlintest:kotlintest-runner-junit5:3.4.2'
    // https://mvnrepository.com/artifact/org.slf4j/slf4j-log4j12
    testImplementation group: 'org.slf4j', name: 'slf4j-log4j12', version: '1.7.25'

}

compileKotlin {
    kotlinOptions.jvmTarget = "1.8"
}
compileTestKotlin {
    kotlinOptions.jvmTarget = "1.8"
}

jar {
    manifest {
        attributes 'Main-Class': 'MainKt'
    }

    from {
        configurations.compileClasspath.collect { it.isDirectory() ? it : zipTree(it) }
    }
}
```

## IntelliJにGrandleインストール, Jar生成まで #

### fatJar ###

```kt
jar {
    manifest {
        attributes 'Main-Class': 'MainKt'
    }

    from {
        configurations.compileClasspath.collect { it.isDirectory() ? it : zipTree(it) }
    }
}
```
> https://qiita.com/MirrgieRiana/items/d3271f6979c1451207a6

> https://qiita.com/shinyay/items/1a000cd082bf2d670531

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

## マルチプロジェクト ##

intelliJでの設定はこれ
> https://qiita.com/kechizenya/items/a7a9e4987304c377d77c

既存モジュールの追加はincludeを`settings.gradle`に入れるだけで良い
`The DefaultSourceDirectorySet constructor has been deprecated.`は気にする必要は無い

## Json ##

https://github.com/google/gson/blob/master/UserGuide.md#TOC-Gson-With-Gradle

```kt
import com.google.gson.Gson

fun main(args: Array<String>) {
    val p = Parent(Child(1,100),20)
    val gson = Gson()

    println(gson.toJson(p))
}

data class Parent(val child: Child, val id: Int)
data class Child(val value: Int, private val value2: Int)
//{"child":{"value":1,"value2":100},"id":20}
```

## OpenCv周り ##

.soはwinだと.dll
System.loadは下の
> https://doitu.info/blog/5c824fd48dbc7a001af33ced

System.loadは下のように絶対パスにする

```kt
System.load(Paths.get("lib/opencv_java420.dll").toAbsolutePath().toString())
```

## ビルド先にファイルをコピー ##

jarタスクでこんな感じにする

```gradle
copy {
    from 'lib/opencv_java420.dll'
    into 'build/libs/lib'
}
```

## IO周り ##

> https://qiita.com/rubytomato@github/items/6880eab7d9c76524d112

## 遅延評価 ##

いわゆるyield

> https://kotlinlang.org/api/latest/jvm/stdlib/kotlin.sequences/-sequence-scope/index.html
