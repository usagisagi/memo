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

## クラス関連 ##

だいたいここ
> https://qiita.com/Kamo123/items/a4c7749fa30d8f68df28


### property関連 ###

```vb
' プロパティプロシージャ
Property Get MyName() As String
    MyName = Name
End Property

Property Let MyName(namae As String)
    If namae = "" Then
        ' 氏名がブランクならエラー
        Err.Raise 10000, , "名前がブランクです"
    End If

    Name = namae
End Property
```