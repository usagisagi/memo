# ubuntu #

## source_code_han_jpのビルド ##
OTF、OTCからビルド済がDLできるのでビルドは不要

## マウスの設定 ##

>sudo apt-get install easystroke

```bash
sudo apt-get install easystroke
```
## Ubuntu 18.04 -> nvidia driver -> CUDA -> cuDNN ##

1. nouveau 無効化

  ```bash
  sudo vi /etc/modprobe.d/blacklist-nouveau.conf
  ```
  viで

  ```
  blacklist nouveau
  optitions nouveau modeset=0
  ```

  読み込んでReboot

  ```bash
  sudo u@date-initranfs -u
  reboot
  ```

1. driverのインストール

  ```bash 
  sudo ubuntu-drivers autoinstall
  sudo reboot
  ```
  secure bootかかるので、Enroll MOK->でpassを入力して入ること

  再起動後、以下のコマンドで確認

  ```bash
  nbidia-smi
  ```

1. cudaのインストール

```bash
  sudo apt install nvidia-cuda-toolkit
  ```
