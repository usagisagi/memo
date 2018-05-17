# ubuntu #

## source_code_han_jpのインストール ##

```sh
[ -d /usr/share/fonts/opentype ] || sudo mkdir /usr/share/fonts/opentype
sudo git clone https://github.com/adobe-fonts/source-code-pro.git /usr/share/fonts/opentype/scp
sudo fc-cache -f -v
```
> https://github.com/adobe-fonts/source-code-pro/issues/17#issuecomment-73454001
