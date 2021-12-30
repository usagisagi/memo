using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;


 class WindowsClipboard {
    private readonly int RETRY_COUNT = 10;
    private readonly int RETRY_DELAY = 100;

    public async Task SetTextAsync(string text, CancellationToken cancellation) {
        await TryOpenClipboardAsync(cancellation);
        InnerSet(text);
    }

    public void SetText(string text) {
        TryOpenClipboard();
        InnerSet(text);
    }

    public async Task<string> GetTextAsync(CancellationToken cancellation) {
        if (!IsClipboardFormatAvailable(cfUnicodeText)) {
            return null;
        }
        await TryOpenClipboardAsync(cancellation);

        return InnerGet();
    }

    public string GetText() {
        if (!IsClipboardFormatAvailable(cfUnicodeText)) {
            return null;
        }
        TryOpenClipboard();

        return InnerGet();
    }

    private void InnerSet(string text) {
        EmptyClipboard();
        IntPtr hGlobal = default;
        try {
            // cb => 確保するメモリのバイト数
            hGlobal = Marshal.AllocHGlobal(cb: (text.Length + 1) * 2);
            if (hGlobal == default) {
                ThrowWin32();
            }

            var target = GlobalLock(hGlobal);
            if (target == default) {
                ThrowWin32();
            }

            try {
                Marshal.Copy(text.ToCharArray(), 0, target, text.Length);
            } finally {
                GlobalUnlock(target);
            }

            if (SetClipboardData(cfUnicodeText, hGlobal) == default) {
                ThrowWin32();
            }

            hGlobal = default;
        } finally {
            if (hGlobal != default) {
                Marshal.FreeHGlobal(hGlobal);
            }

            CloseClipboard();
        }
    }

    private async Task TryOpenClipboardAsync(CancellationToken cancellation) {
        for (int i = 0; i < RETRY_COUNT; i++) {
            if (OpenClipboard(default)) {
                return;
            }

            await Task.Delay(RETRY_DELAY, cancellation);
        }

        ThrowWin32();
    }

    private void TryOpenClipboard() {
        for (int i = 0; i < RETRY_COUNT; i++) {
            if (OpenClipboard(default)) {
                return;
            }

            Thread.Sleep(RETRY_DELAY);
        }

        ThrowWin32();
    }

    private string InnerGet() {
        IntPtr handle = default;
        IntPtr pointer = default;
        try {
            handle = GetClipboardData(cfUnicodeText);
            if (handle == default) {
                return null;
            }

            pointer = GlobalLock(handle);
            if (pointer == default) {
                return null;
            }

            var size = GlobalSize(handle);
            var buff = new byte[size];

            Marshal.Copy(pointer, buff, 0, size);

            return Encoding.Unicode.GetString(buff).TrimEnd('\0');

        } finally {
            if (pointer != default) {
                GlobalUnlock(handle);
            }

            CloseClipboard();
        }
    }

    const uint cfUnicodeText = 13;

    static void ThrowWin32() {
        throw new Win32Exception(Marshal.GetLastWin32Error());
    }

    [DllImport("User32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool IsClipboardFormatAvailable(uint format);

    [DllImport("User32.dll", SetLastError = true)]
    static extern IntPtr GetClipboardData(uint uFormat);

    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr GlobalLock(IntPtr hMem);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool GlobalUnlock(IntPtr hMem);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool OpenClipboard(IntPtr hWndNewOwner);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    static extern bool CloseClipboard();

    [DllImport("user32.dll", SetLastError = true)]
    static extern IntPtr SetClipboardData(uint uFormat, IntPtr data);

    [DllImport("user32.dll")]
    static extern bool EmptyClipboard();

    [DllImport("Kernel32.dll", SetLastError = true)]
    static extern int GlobalSize(IntPtr hMem);
}


