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

## 重複削除 ##

```vb
Private Function UniqueArray(Arr() As String) As String()
    ' 重複を削除
    Dim BufCollection As New Collection
    Dim IsExist As Boolean
    Dim Item As Variant
    
    For i = LBound(Arr) To UBound(Arr)
        IsExist = False
        For Each Item In BufCollection
            If Arr(i) = Item Then IsExist = True
        Next
        If Not IsExist Then BufCollection.Add Arr(i)
    Next

    'キー項目の配列を返す
    UniqueArray = CollectionToArray(BufCollection)
    
End Function
Public Function CollectionToArray(myCol As Collection) As String()
    Dim result() As String
    Dim cnt     As Long
    ReDim result(myCol.Count - 1)

    For cnt = 0 To myCol.Count - 1
        result(cnt) = myCol(cnt + 1)
    Next cnt

    CollectionToArray = result
End Function


```