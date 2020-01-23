# Kotlin: マルチモジュール構成方法 #

1. 何も依存しないGradleのモジュールを作成する。(Rootとなる)

1. サブモジュールを作成する

1. 作成したサブモジュールに以下のディレクトリ構造を作成する

```
./src
./src/main
./src/main/kotlin
./src/main/resources
./src
./src/test
./src/test/kotlin
./src/test/testResources
```

1. サブモジュール名をRootの`settings.gradle`にincludeして記述

1. さらにサブモジュールを作る

1. そのサブモジュールを既存のモジュールに依存させるには、`compile project("$projectName")`を`build.gradle`の`dependency`に追加するだけで良い

