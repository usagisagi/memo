# Scala #

## PDFBox ##

公式
>https://pdfbox.apache.org/

>http://www.w3ii.com/ja/pdfbox/default.html

## 列挙型 ##

```scala
sealed trait SampleEnum
 
case object A extends SampleEnum
case object B extends SampleEnum
case object C extends SampleEnum
case object D extends SampleEnum
```

> https://dev.classmethod.jp/server-side/scala-algebra-data-type/


## BufferedImage ##

### 画像表示 ###

> https://www.javadrive.jp/java2d/bufferedImage/index2.html

```scala
import java.io.File
import javax.imageio.ImageIO
import java.awt.Image
import java.awt.image.{BufferedImage, DataBufferByte}
import java.awt.Dimension

val file = new File("Lenna.jpg")
val img = ImageIO.read(lennaFile)

def shImg(img: Image, title: String): Unit = {
  val frame = new JFrame(title)

  val icon = new ImageIcon(img)
  val disp = new JLabel(icon)
  frame.add(disp)

  val frameSize = new Dimension(icon.getIconWidth, icon.getIconHeight)
  frame.setSize(frameSize)
  frame.setVisible(true)
}
```

### 画像のresize ###

```scala
private def resizeImg(img: Image): Image = {
  val height = ImageHeight
  val width = floor(img.getWidth(null) * (ImageHeight / img.getHeight(null).toFloat)).toInt
  // 入れ物となるBufImage
  val bufImg = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB)
  bufImg.getGraphics.drawImage(
    img.getScaledInstance(width, height, Image.SCALE_AREA_AVERAGING),
    0, 0, width, height, null)
  bufImg.asInstanceOf[Image]
}
```

### 色空間の変換 ###

一度作って書き込む

> https://stackoverflow.com/questions/6881578/how-to-convert-between-color-models

```scala
def convertImgType(src: BufferedImage, bufImgType: Int): BufferedImage = {
  val img = new BufferedImage(src.getWidth(), src.getHeight, bufImgType)
  val g2d = img.createGraphics
  g2d.drawImage(src, 0, 0, null)
  g2d.dispose()
  img
}
```



## openCVJava ##

Documentation

> https://docs.opencv.org/

tutorial

> http://opencv-java-tutorials.readthedocs.io/en/latest/index.html

### install ###

<s>プロジェクト構造から`.dll`と`jar`を指定する。</s>
パスを通す
-Djava.library.path={libへのパス}


### Template Matching ###

> https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html

![img](img/opencv_scala_install.png)

### BufferedImageToMat ###

> https://qiita.com/hahegawa/items/9dbe09c2c44b60f36cfc

```scala
private def convBufferedImageToMat(src: BufferedImage): Mat ={
val dst: Mat = new Mat(src.getHeight(), src.getWidth(), CvType.CV_8UC3)
val bin: Array[Byte] = src
    .getRaster
    .getDataBuffer
    .asInstanceOf[DataBufferByte] 　0b2

dst.put(0,0,bin)
dst
}
```

### 最初のページ画像を原寸で取得 ###

```scala
def extractImage(document: PDDocument): Option[BufferedImage] = {
  val resources = document.getDocumentCatalog.getPages.get(0).getResources
  val ite = resources.getXObjectNames.iterator()

  if (ite.hasNext){
    val name = ite.next()
    resources.getXObject(name) match {
      case xobject: PDImageXObject => Option(xobject.getImage)
      case _ => None
    }
  } else {
    None
  }
}
```

## Matの表示 ##

```scala
import java.awt.Image
import java.awt.image.BufferedImage

import javax.swing.{ImageIcon, JFrame, JLabel}
import org.opencv.core.{CvType, Mat}
import org.opencv.highgui.HighGui

def shImg(img: Image, title: String): Unit = {
val frame = new JFrame(title)
val icon = new ImageIcon(img)
val disp = new JLabel(icon)
frame.add(disp)
frame.pack()
frame.setVisible(true)
}

def shImg(mat: Mat, title: String): Unit = {
val img: Image = HighGui.toBufferedImage(mat)
shImg(img, title)
}
```

## クラス関連 ##

### traitのフィールドのオーバーライド ##

オーバーライド先のvalを`lazy val`にして評価を強制する

```scala
trait FruitTree {
    def fruit: String
    val descriptor = new FruitTreeDescriptor(fruit)
}

object BananaTree extends FruitTree {
    /**/
    lazy val fruit = "banana"
}
```

## 酢豚の作り方 ##

1. `project`直下（`build.propaties`があるところ）にplugin.sbtを作成し以下のコードを入力。
    **（たまにバージョンが上がっていないか確認する事）**

    ```scala
    addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "0.14.6")
    ```
2. `build.sbt`に以下のコードを入力

    ```scala
    mainClass in assembly := Some({mainClassName})
    ```

3. sbt shellで`assembly`を実行

4. 実行時に`jar -cp {jarfile} {mainclassname}`

## 並列スレッド数の設定法 ##

パフォーマンスは並列稼動数と等しい時に最高になる

```scala
    System.setProperty("scala.concurrent.context.numThreads", xxx)
    System.setProperty("scala.concurrent.context.maxThreads", xxx)

    println( s"Core: ${collection.parallel.availableProcessors}")
```

## 型について ##

### UnionType ###

Scalaが標準でもつ型と論理の対応は次のようになる.

|型|論理|
|:--|:--|
|Any|真|
|Nothing|偽|
|A => B|A ならば B|
|A with B|A かつ B|
|P[A] forSome { type A } |P[A] である A が存在する|

型の包含関係は次のように記述できる.

```scala
// AはAに含まれる
A <:< A
// AかつBはAに含まれる
A with B <:< A
// AかつBはBに含まれる
A with B <:< B
```

```scala
// Aならば偽。Function1なのでちゅうい
type Not[A] = A => Nothing

// （A￢∩B￢)￢ => (A∪B) [ド・モルガンの法則]
type Or[A, B] = Not[Not[A] with Not[B]]

// Or[Int, String]はFunction1なので、元もFunction1のNot[Not[A]]にする
def double[A](a: A)(implicit ev: Not[Not[A]] <:< Or[Int, String]): String =
  a match {
    case i: Int => (i + i).toString
    case s: String => s + s
  }

assert(double(2) == "4")
assert(double("2") == "22")
```

>  http://halcat.org/scala/curryhoward/index.html