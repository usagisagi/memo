# PyTorch #

## マルチプロセス絡みのエラー ## 

+ loaderのnum_workersを0にする。学習時はmultiになるので安心すること。

> https://pytorch.org/docs/stable/notes/windows.html#usage-multiprocessing