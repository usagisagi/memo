# Moq #

## 引数の値を利用してメソッドを設定 ##

Returns メソッドには 4 引数まで取るオーバーロードが用意されてるので、モックメソッドの引数の値を利用できます。

```cs
// int Foo(int x, int y) というメソッドで、x * y を返す
mock.Setup(p => p.Foo(It.IsAny<int>(), It.AsAny<int>())).Returns((int x, int y) => x * y);
```
