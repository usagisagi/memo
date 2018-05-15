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

1. jQueryをjsフォルダ内にいれる
