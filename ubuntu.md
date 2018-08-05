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

## pycharmでtensorflowを動かす ##

起動構成に環境変数を追加する

```
LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

後Permission700で以下のフォルダを作る

```
/run/user/1000/snap.pycharm-community
```
## Tensorflowを再インストール ##

```bash
pip uninstall tensorflow protobuf --yes
find $CONDA_PREFIX -name "tensorflow" | xargs -Ipkg rm -rfv pkg
pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.9.0-cp36-cp36m-linux_x86_64.whl --no-cache-dir
```

### Ubuntu 18.04にScalaとSbtとJavaをインストール ###

```bash
sudo add-apt-repository ppa:webupd8team/java
sudo apt update
sudo apt install oracle-java8-installer
sudo apt install oracle-java8-set-default
javac -version


```

> http://www.codebind.com/linux-tutorials/install-scala-sbt-java-ubuntu-18-04-lts-linux/

## UbuntuにOpenCVをインストール ##

きついけど頑張れ
javaのパスに注意

> https://github.com/opencv-java/opencv-java-tutorials/blob/master/docs/source/01-installing-opencv-for-java.rst


## mysql ##

### インストール ###

> http://yikedd.iteye.com/blog/2422566

設定したらrebootする

以下メモ

```markdown
`mysqld --verbose --help`でオプションが見られる

> https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-ubuntu-18-04

+ `mysqld`は`sudo`で動かない
  `sudo chmod 777 /var/log/mysql/error.log`で権限を変更する

### uninstall ###

```bash
sudo apt-get remove --purge mysql-server* mysql-common 
sudo apt-get autoremove --purge 
sudo rm -r /etc/mysql
sudo rm -r /var/lib/mysql
```
### 停止開始再起動 ###

`sudo /etc/init.d/mysql [start/stop/restart]`

### 移動時のpermission denied ###

> https://askubuntu.com/questions/844614/16-04-cant-mysqld-initialize-in-non-default-location

> https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-18-04

```sh
sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
cd /etc/apparmor.d/disable
sudo ln -s /etc/apparmor.d/usr.sbin.mysqld .
```

SELinuxが邪魔する
> http://enakai00.hatenablog.com/entry/20121112/1352693845

```