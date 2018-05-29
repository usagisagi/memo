# Bootstrap #

まずはじめにjQueryをjsフォルダ内にいれる

## リンク ##

使い方が詳しい
> https://www.tuyano.com/

日本語のテーマ
> http://honokak.osaka/

## Select2 ##

### Usage ###

header

```html
<script src="./js/select2.min.js"></script>
```

form_component

``` html
<select class="basic-single form-control" name="myform">
<option value="Hokaido">北海道</option>
<option value="Tokyou">東京</option>
<option value="Osaka">大阪</option>
<option value="Fukuoka">福岡</option>
<option value="Okinawa">沖縄</option>
</select>   
```

### select時にsubmit ###

script
```html
    <script type="text/javascript">
        $(function () {
            //select2化
            $('.basic-single').select2();
            $('.basic-single').change(function () {
                document.myform.submit();
            }
            )
        });
    </script>
```

Form
```html
<form action="#" method="POST", name="myform">
    <select class="basic-single form-control" name="myform">
        <option value="Hokaido">北海道</option>
        <option value="Tokyou">東京</option>
        <option value="Osaka">大阪</option>
        <option value="Fukuoka">福岡</option>
        <option value="Okinawa">沖縄</option>
    </select>
</form>
```

## 表示と非表示を切り替える ##

script

```js
<script language="JavaScript">
function reverse_display(form_id1, form_id2)
{
    // 表示を反転させる
    var obj1 = document.getElementById(form_id1).style;
    obj1.display = (obj1.display == 'none') ? 'block' : 'none';

    var obj2 = document.getElementById(form_id2).style;
    obj2.display = (obj2.display == 'none') ? 'block' : 'none';

    return false;
}
</script>
```

python側

```python       
def generate_reverse_link(div_id: str, div_id_all: str, before_text: str, after_text: str):
    """
    折り畳みボタンのリンクを作成する

    :param div_id:
        折り畳み前のテキストを示すdivのid
    :param div_id_all:
        折り畳み後のテキストを示すdivのid
    :param before_text:
    :param after_text:
    :return:
        htmlコード
    """
    return \
    f"""
    <div id="{div_id}" class="">
        <a href='javascript:void(0)' onclick='reverse_display("{div_id}","{div_id_all}")'>
            {before_text}
        </a>
    </div>
    <div id="{div_id_all}" class="" style="display: none;">
        <a href='javascript:void(0)' onclick='reverse_display("{div_id}","{div_id_all}")'>"
            {after_text)}
        </a>
    </div>
    """
```

## クリックでイベントを起動して -> post値を変更


```js
$(function(){
    $(".jump").on('click',function(event){
        event.preventDefault();
        event.stopPropagation();
        location.href = 'http://hoge' + $(this).attr('href');
        return false;
    });
});
```

```html
<a href="1" class="jump">ページ１</a>
<a href="2" class="jump">ページ２</a>
```

## Ajaxの非同期読み込み ##

> http://www.alt-plus.jp/archives/360
> 
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Ajaxを用いたプルダウンサンプル</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>

<script type="text/javascript">
<!--
function getTableData() {
    //プルダウンで選択されたValueを取得
    var selectVal = $("#team_id").val();
    //getJSONで、別途用意している処理用PHPに必要な値を投げて受け取ります
    $.getJSON("http://www.alt-plus.jp/sandbox/hachi/20150629_ajaxsample/getdata.php"
            , {"team_id": selectVal }            //team_idに取得したValue値を投げます
            , function (data, status) {
                var playerList = $("#player_id");    //連動するプルダウンのID
                playerList.children().remove();    //子要素は毎回全て削除します(初期化)
                for (i in data) {
                    var row = data[i];
                    //取得したデータをAppendで1行ずつ追加
                    playerList.append(new Option(row['player_name'], row['player_id']));
                }
             }
             /*****エラーハンドリング用
             ).success(function(json) {
                console.log("成功");
            }).error(function(jqXHR, textStatus, errorThrown) {
                console.log("エラー：" + textStatus);
                console.log("テキスト：" + jqXHR.responseText);
            }).complete(function() {
                console.log("完了");
            }
*/
     );
}
</script>
</head>
<body>
<select id="team_id" name="team_id" onchange="getTableData()">
    <option value="">--チームを選択してください--</option>
    <option value="1">読売ジャイアンツ</option>
    <option value="2">中日ドラゴンズ</option>
</select>
<select id="player_id" name="player_id">
    <option value="">--選手を選択してください--</option>
</select>
</body>
</html>
```

### 行の追加 ###

```JS
addRow = function() {
    $('#nameTable tr:last').after('<tr><td>山下</td><td>28</td></tr>');
}
```

getdata.php

```php
//クライアントから送信されるチームIDを取得します
$team_id = $_GET['team_id'];

//クライアントに返す検索結果はこいつに入れます
$response = array();

//DBからチームIDに合致する選手名を取得します
if (strlen($team_id) != 0) {
    $link = mysql_connect('DBの場所', 'DBユーザ', 'DBパスワード');
    mysql_select_db('使用するDB名');
    mysql_query("SET NAMES utf8", $link);
    $sql  = "SELECT player_id";
    $sql .= "     , player_name";
    $sql .= "  FROM テーブル名";
    $sql .= sprintf(" WHERE team_id = '%s'", mysql_real_escape_string($team_id));
    $sql .= " ORDER BY player_id ASC";
    $result = mysql_query($sql, $link);
    while ($row = mysql_fetch_array($result, MYSQL_ASSOC)) {
        array_push($response, $row);
    }
}
//JSON形式で値を返します
echo(json_encode($response));
```

## DataTables ##

### 日付等の並び替え ###

`<td>`タグに`data-order`属性を仕込んで並び替えをj指示するだけ(らくちーん)
`<thead>`には仕込みは不要

```html
<tr>
    <td data-search="Airi Satou">A. Satou</td>
    <td>Accountant</td>
    <td>Tokyo</td>
    <td>33</td>
    <td data-order="1227830400">Fri 28th Nov 08</td>
    <td data-order="162700">$162,700/y</td>
</tr>
```

> https://datatables.net/examples/advanced_init/html5-data-attributes.html

### DataTables絡み ###

基本の使い方

> https://qiita.com/nissuk/items/7ac59af5de427c0585c5

Ajax絡み

> https://datatables.net/examples/ajax/orthogonal-data.html

#### 並び替え ####

以下の様にする

```js
$(document).ready(function() {
    $('#example').DataTable( {
        ajax: "data/orthogonal.txt",
        columns: [
            { data: "name" },
            { data: "position" },
            { data: "office" },
            { data: "extn" },
            { data: {
                _:    "start_date.display",
                sort: "start_date.timestamp"
            } },
            { data: "salary" }
        ]
    } );
} );
```

```html
<table id="example" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Office</th>
                <th>Extn.</th>
                <th>Start date</th>
                <th>Salary</th>
            </tr>
        </thead>
        <tfoot>
            <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Office</th>
                <th>Extn.</th>
                <th>Start date</th>
                <th>Salary</th>
            </tr>
        </tfoot>
    </table>
```

```json
{
  "data": [
    {
      "name": "Tiger Nixon",
      "position": "System Architect",
      "salary": "$320,800",
      "start_date": {
        "display": "Mon 25th Apr 11",
        "timestamp": "1303689600"
      },
      "office": "Edinburgh",
      "extn": "5421"
    },
}
```


