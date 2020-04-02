# DIContainer #

> https://qiita.com/TsuyoshiUshio@github/items/20412b36fe63f05671c9


## SetUp ##

以下の2つのNuGetパッケージをインストールする。

```
Microsoft.Extensions.DependencyInjection
Microsoft.Extensions.DependencyInjection.Abstraction
```

## Usage ##

```cs
var sc = new ServiceCollection();
sc.AddSingleton<IService, Service>();
var p = sc.BuildServiceProvider();
var s = p.GetRequiredService<IService>();
```
