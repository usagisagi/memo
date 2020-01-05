# CSharp #

## フォームコントロール ##
### BackGroundWorker ###
```C#
using System;
using System.ComponentModel;
using System.Threading;
using System.Windows.Forms;

namespace Chap16 {
    public partial class Form1 : Form {
        private BackgroundWorker _worker = new BackgroundWorker();

        public Form1() {
            InitializeComponent();
            _worker.DoWork += _worker_DoWork;
            _worker.RunWorkerCompleted += _worker_RunworkerCompleted;
            _worker.ProgressChanged += _worker_ProgressChanged;
            _worker.WorkerReportsProgress = true;
        }

        private void _worker_DoWork(object sender, DoWorkEventArgs e) {
            for (var i = 1; i <= 10; i++) {
                Thread.Sleep(500);
                // 第二引数(UserState)にobjectを渡すことができる
                _worker.ReportProgress(1, "うさぎ");
            }
        }

        private void _worker_ProgressChanged(object sender, ProgressChangedEventArgs e) {
            // _worker_DoWorkへ渡したobjectを受け取ることができる
            button1.Text = e.UserState.ToString();
        }

        private void _worker_RunworkerCompleted(object sender, RunWorkerCompletedEventArgs e) {
            button1.Text = "終了";
        }

        private void Button1_Click(object sender, EventArgs e) {
            button1.Text = "処理中";
            _worker.RunWorkerAsync();
        }
    }
}

```

### マウスをクリックする ###

```C#
private class MouseSimulate {
    private const UInt32 MOUSEEVENTF_LEFTDOWN = 0x0002;
    private const UInt32 MOUSEEVENTF_LEFTUP = 0x0004;

    [DllImport("USER32.dll", CallingConvention = CallingConvention.StdCall)]
    private static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, uint dwExtraInf);

    public static void SimulateLeftClick(int x, int y) {
        Cursor.Position = new System.Drawing.Point(x, y);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
}
```

### Internal属性のテストを行う ###

テスト**対象**プロジェクトの`AssemblyInfo.cs`に`[assembly: InternalVisibleTo("XXXX")]`を追加。

**XXXXはテストプロジェクトのアセンブリ名**

## Sprache ##

### XOR ###

`first.Xor(Second)`

firstで1文字でもtrueと評価のち、falseになったらsecondにかかわらずfalse

firstで最初の文字だけ異なる場合secondを評価する

### ChainOperator ###

```cs
public static Parser<T> ChainOperator<T, TOp>(Parser<TOp> op, Parser<T> operand, Func<TOp, T, T, T> apply);
```

1. 以下のParserでParse
```cs
from leftOperand in operand
from operator in op
from rightOperand in operand
select apply(operator, leftOperand, rightOperand)
```

1. Parseできなかったら`operand`でParse

## DataBase周り ##

### bulkInsert ###

DataTable作る => カラム名の列を作る => BulkInsertインスタンスを作る => 投入

```CS
using System;
using System.Data;
using System.Data.SqlClient;
namespace Sample {
    
    public class MainProcess {
        
        [STAThread]
        public static void Main(string[] args) {
            
            System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
            sw.Start();
            
            var m = new MainProcess();
            m.StartProcess();
            
            sw.Stop();
            Console.WriteLine(sw.Elapsed);
        }
        
        private void StartProcess() {
            
            string connectionString = "Data Source=192.168.1.5\\SQLEXPRESS;Initial Catalog=sample;User ID=sa;Password=P@ssw0rd";
            
            Console.WriteLine("Start");
            
            DataTable table = new DataTable("Table_1");
            table.Columns.Add(new DataColumn("id", typeof(int))); 
            table.Columns.Add(new DataColumn("name", typeof(string)));
            for(int i = 1; i <= 10000; i++) {
                table.Rows.Add(i, "テストデータ");
            }
            using(SqlBulkCopy bulkCopy = new SqlBulkCopy(connectionString)) {
                bulkCopy.BulkCopyTimeout = 600; // in seconds
                bulkCopy.DestinationTableName = "Table_1";
                bulkCopy.WriteToServer(table);
            }
            
            Console.WriteLine("End");
        }
    }
}
```

> https://symfoware.blog.fc2.com/blog-entry-1186.html

## C#コレクション計算量一覧 ##

||データ構造|追加|取得|検索|ソート|列挙|削除|集合演算|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
|List\<T\>|配列|O(1)|O(1)|O(n)|O(nlogn)|O(1)|O(n)|-|
|LinkedList\<T\>|連結リスト|O(1)|O(n)|O(n)|-|O(1)|O(n)（要素指定）<br>O(1)（ノード指定）|-|
|Queue\<T\>|循環配列|O(1)（enQ）|O(1)（peek, deQ）|O(n)|-|-|O(1)（deQ）|-|
|Stack\<T\>|配列|O(1)（push）|O(1)（peek, pop）|O(n)|-|-|O(1)（pop）|-|
|Dictionary\<TKey, TValue\>|ハッシュテーブル|O(1)|O(1)|O(1)|-|-|O(1)|-|
|HashSet\<T\>|ハッシュテーブル|O(1)|-|O(1)|-|O(1)|O(1)|O(n+m)|
|SortedDictionary\<TKey, TValue\>|二部探索木|O(nlogn)|O(logn)|O(logn)|-|O(logn)|O(logn)|-|
|SortedList\<TKey, TValue\>|配列|O(n)|O(logn)|O(logn)（key）<br>O(logn)（index）|-|O(1)|O(n)|-|
|SortedSet\<T\>|二部探索木|O(logn)||O(logn)|-|O(logn)|O(logn)|O(n+m)|

> https://qiita.com/takutoy/items/37e81b916271bf43b527#sortedsett

## コマンドラインパーサ ##

> https://qiita.com/skitoy4321/items/742d143b069569014769

## EntityFramework v6.x ##

## Migrationのやり方 ##

1. `SQL Server オブジェクト エクスプローラ`でデータベース作成
1. 新しい項目を追加 
1. `ADO.NET Entity Data Model`
1. データベースからCode First
1. 新しい接続 -> データソースを`Microsoft SQL Server` -> サーバ名を`(localdb)\MSSQLLocalDB`
1. 作成したデータベースを選択
1. データベース定義を書く
1. 以下のコマンドを打つ
```
EntityFramework\Enable-Migrations
EntityFramework\add-migration ${名前}
EntityFramework\Upgrade-Database
```



### EntityFrameworkでエラーを吐いたとき ###

`EntityFramework.SqlServer.dll`がなぜか出力ファイルにコピーされていない。
コピーする。


### 接続文字列が見つからない ###

VS2017 Update-Databaseで XXX という名前の接続文字列がアプリケーション構成ファイルに見つかりませんでした。と言われたら
該当プロジェクトをスタートアッププロジェクトにしたら解決。

### 標準入出力 ###

```cs
var pInfo = new ProcessStartInfo {
    FileName = treeTaggerPath.FullName,
    Arguments = $"\"{parPath.FullName}\" {opts}",
    CreateNoWindow = true,
    UseShellExecute = false,
    RedirectStandardOutput = true,
    RedirectStandardInput = true,
    RedirectStandardError = true
};

using (var process = Process.Start(pInfo)) {
    using (var writer = process.StandardInput) {
        process.ErrorDataReceived += Process_ErrorDataReceived;
        writer.AutoFlush = true;
        writer.Write(string.Join("\n", words)); // 多分これが最速
    }
    var results = process.StandardOutput.ReadToEnd();
    process.WaitForExit();

    return results
        .Split(new string[] { "\r\n", "\n" }, StringSplitOptions.RemoveEmptyEntries)
        .Select(s => s.Split('\t')[2])
        .Select(s => s.Split('|').First());
}
```

## 入れ子の型 ##

コンストラクタで外側の型を渡すことで、外側の型のprivate memberにアクセスできる。


```cs
class Outer {
    int value = 100;
    class Inner {
        Outer outer;

        public Inner(Outer outer) {
            this.outer = outer;
        }

        public void run() {
            this.outer.value = 100;
        }
    }
}
```
