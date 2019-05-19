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
