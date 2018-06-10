# MX MASTER S2 In Ubuntu Memo #

## マウス自体の設定[dpi, etc, ...] ##

solaarで設定する。**gitから落とさないとMX Master S2 は反応しない**
> https://github.com/pwr/Solaar.git

依存関係が色々あるのでややこしいが手動で頑張ってインストールする。

```
git clone https://github.com/pwr/Solaar.git
sudo apt-get install python3-pyudev python3-gi gir1.2-gtk-3.0
cd rules.d
sudo sh install.sh
```

(girとかはいらないかも)

以下のコマンドでペアリング（だけど自分は自動認識されてた）。

```
sudo python bin\solaar pair
```

あとは`show`や`pair`を使えばdpiの設定などができる。

+ ボタン割当

    |物理的な操作|認識されるイベント|
    |---|---
    |左ボタン|button 1|
    |ホイールボタン|button 2|
    |右ボタン|button 3|
    |ホイールを上に回す|button 4|
    |ホイールを下に回す|button 5|
    |ホイール近くの "i" ボタン|Linuxでは認識されません<br/>フリースピン可否の切り替えは可能|
    |サムホイールを右 (上) に回す|button 6|
    |サムホイールを左 (下) に回す|button 7|
    |サイドの下側ボタン|button 8|
    |サイドの上側ボタン|button 9|
    |親指ボタン|Ctrl+Alt+Tab<br/><変更不可>|

    > https://wiki.archlinux.jp/index.php/Logitech_MX_Master

+ ボタンの割当

    + Ctrl + Alt + Tab

        Ubuntuだと`システムのコントロールを切り替える`だけどあまり使わない。ので、Grobal Shortcutsの割当を変更することに。`デバイス -> キーボード`でショートカットを設定できる。

        私はアクティビティ画面を表示するにしました。

    + ボタンの割当
        色々ソフトがあるけど`xbindkeys`と`xautomation`を使ってみる。

        インストールはapt-get

        ```sh
        sudo apt-get xbindkeys xautomation
        ```

        `xbindskeys`はボタンの割当を行うソフト。コマンドを割り当てることができる。`xautomation`はキーの送信をエミュレートするソフト。`xbindskey`でこのソフトのコマンドを叩くことでエミュレートする。

        homeに`.xbindkeys`ファイルを作成し、1行目`コマンド`、2行目`b:{割当たいボタン番号}`のように記述する。`xautomation`の`xte`コマンドは`xbindkeys -k`で確認できる。

        ```sh
        # 親指チルト上方向で ctrl + pageup
        # xautomationを利用
        "xte `Control+Mod2 + Prior`"
            b:6

        # 親指チルト上方向で ctrl + pagedown
        "xte `Control+Mod2 + Next`"
            b:7
        ```

        > https://wiki.archlinux.jp/index.php/Logitech_MX_Master
        > https://wiki.archlinux.jp/index.php/Xbindkeys

        以下のコマンドで起動
        ```sh
        xbindskey
        pkill xbindskey 
        ```


+ 挙動の確認
    ```
    xev | grep button
    ```
    > http://mattintosh.hatenablog.com/entry/20161016/1476546334