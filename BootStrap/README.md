# Bootstrap #

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
</sceript>
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
        <a href='javascript:void(0)' onclick='reverse_display(\"{div_id}\",\"{div_id_all}\")'>
            {before_text}
        </a>
    </div>
    <div id="{dvi_id_all}" class="" style="display: none;">
        <a href='javascript:void(0)' onclick='reverse_display(\"{div_id}\",\"{div_id_all}\")'>"
            {after_text)}
        </a>
    </div>
    """
```


1. jQueryをjsフォルダ内にいれる
