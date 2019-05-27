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
