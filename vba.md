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

## テキストファイル読み込み ##

```vb
Open "C:\Sample\Data.txt" For Input As #1
    Do Until EOF(1)
        Line Input #1, buf
        セル = buf
    Loop
Close #1
```