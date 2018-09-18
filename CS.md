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
