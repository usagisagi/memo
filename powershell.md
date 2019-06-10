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

```sh
$ pandoc --print-default-data-file reference.docx > reference.docx
```

作成された reference.docx ファイルを Word で開いて、スタイルを編集します。

- Heading 1〜6 や 本文 など、使われるスタイル。
- ヘッダーやフッター
本文の内容は無視されるので、消す必要はありません。

#### docx ファイルの作成 ####
作成したテンプレートを使って、新しい docx ファイルを作成します。

```sh
$ pandoc new.md --reference-docx=reference.docx -s -o new.docx
```

作成された new.docx のレイアウトが reference.docx で指定したものになっていれば OK です。

> http://www.minimalab.com/blog/2016/08/16/convert-md-to-docx/
