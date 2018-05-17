# VBA #

## テキストファイルの書き出し ##

```vb
Open "C:\Sample\Data.txt" For Append As #1
    Print #1, "桜木"
Close #1
```

> http://officetanaka.net/excel/vba/file/file08c.htm

## 自分自身のフォルダを取得 ##

```vb
Application.CurrentProject.Path
```