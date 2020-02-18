# PowerShell #

## convert to UTF8 (BOMなし) ##

### powershell native ###

Out-Stringを使って明示的に改行込みの文字列にする
例2と異なり -Raw オプションが付いていないのに注意

```ps
Get-Content -Path ".\Source.txt" -Encoding Default `
    | Out-String `
    | % { [Text.Encoding]::UTF8.GetBytes($_) } `
    | Set-Content -Path ".\BOMlessUTF8.txt" -Encoding Byte
```

### nkf ###

パイプでつないだ瞬間なぜか文字化けするので注意

```ps
nkf --overwrite --oc=UTF-8 ExportFullText.txt 
```
## pandoc ##

### テンプレートの編集 ###

#### 準備 ####

まずはテンプレートの docx ファイルを作成します。

**cmdで実行すること！パワーシェルだと破損する！**

```sh
$ pandoc --print-default-data-file reference.docx > reference.docx
```

作成された reference.docx ファイルを Word で開いて、スタイルを編集します。

使用できるスタイルは以下の通り：

【段落】
標準(Normal), Compact, 表題(Title), Authors, 日付(Date), Heading 1, Heading 2, Heading 3, Heading 4, Heading 5, Block Quote, Definition Term, Definition, 本文(Body Text), Table Caption, Image Caption; 

【文字】 Default Paragraph Font, Body Text Char, Verbatim Char, Footnote Ref, Link.

- Heading 1〜6 や 本文 など、使われるスタイル。
- ヘッダーやフッター
本文の内容は無視されるので、消す必要はありません。

#### docx ファイルの作成 ####

作成したテンプレートを使って、新しい docx ファイルを作成します。**なんか知らないけどVS-CODEの拡張機能はバグるのでダメ**

```sh
$ pandoc new.md --reference-docx=reference.docx -s -o new.docx
```

作成された new.docx のレイアウトが reference.docx で指定したものになっていれば OK です。

> http://www.minimalab.com/blog/2016/08/16/convert-md-to-docx/
> https://qiita.com/sky_y/items/5fd5c9568ea550b1d7af

## 正規表現でファイルを検索して移動 ##

```
Get-ChildItem -Recurse -File | where {$_ -match ".*GS.*" } | Move-Item -Destination .\GS
```
