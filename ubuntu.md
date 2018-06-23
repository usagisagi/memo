# ubuntu #

## source_code_han_jpのビルド ##
OTF、OTCからビルド済がDLできるのでビルドは不要

## マウスの設定 ##

>sudo apt-get install easystroke

```bash
sudo apt-get install easystroke
```
## Ubuntu 18.04 -> nvidia driver -> CUDA -> cuDNN ##

1. ubuntuインストール時にサードパーティ有効化し、`Trun off Secure Boot`にチェック

1. インストール後再起動し、MOK青画面でChange Secure Boot-でYesを選択する

1. driverのインストール

  ```bash 
  sudo ubuntu-drivers autoinstall
  sudo reboot
  ```
  インストール途中止まったら、UEFIのパスワードを入力すること

  再起動後、以下のコマンドで確認

  ```bash
  nbidia-smi
  ```

1. cuda9.0のインストール
 https://medium.com/@taylordenouden/installing-tensorflow-gpu-on-ubuntu-18-04-89a142325138
 
## PermissionDenied ##

`sudo chown -R usagisagi:usagisagi /home/usagisagi/anaconda3`
