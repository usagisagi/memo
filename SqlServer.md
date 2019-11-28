# SQLServer #

## インデックスのチューニング ##

```sql
SELECT gs.last_user_seek AS [最後にシークした時間],
       id.statement AS [テーブル名] ,
       id.equality_columns AS [等値述語に使用できる列],
       id.inequality_columns AS [不等値述語に使用できる列] ,
       id.included_columns AS [包括列として必要な列],
       gs.unique_compiles AS [コンパイルおよび再コンパイルの数],
       gs.user_seeks AS [クエリによって発生したシーク数]
 FROM  sys.dm_db_missing_index_group_stats AS gs
       INNER JOIN sys.dm_db_missing_index_groups AS ig
			ON gs.group_handle = ig.index_group_handle
       INNER JOIN sys.dm_db_missing_index_details AS id
			ON ig.index_handle = id.index_handle
 WHERE id.[database_id] =DB_ID() Order By gs.last_user_seek ASC
```

包含列を含まれている列として設定し、非クラスター化インデックスとして作成。

> http://ryuchan.hatenablog.com/entry/2013/09/23/134554

包含列（付加列インデックス）について。終着ノード（リーフノード）にくっついているデータのこと。

> https://qiita.com/KimiguS/items/0519005915d658081131

## 全インデックスの再構成 ##

```tsql
DECLARE @TableName sysname, @IndexName sysname
DECLARE @basesql nvarchar(max), @sql nvarchar(max)
DECLARE @Edition nvarchar(max)

SET @Edition = CONVERT(nvarchar, SERVERPROPERTY('Edition'))

SET @basesql = 'ALTER INDEX @1 On @2 REBUILD @3'

IF PATINDEX('%Enterprise%', @Edition) > 0
BEGIN
    SET @basesql = REPLACE(@basesql, '@3', 'WITH (ONLINE=ON)')
END
ELSE
    SET @basesql = REPLACE(@basesql, '@3', '')

DECLARE IXC CURSOR FOR
SELECT
    OBJECT_NAME(object_id) AS TableName
    , name AS IndexName
FROM
    sys.indexes
WHERE
    OBJECT_SCHEMA_NAME (object_id) <> 'sys'
    AND
    index_id > 0
ORDER BY 1

OPEN IXC

FETCH NEXT FROM IXC
INTO @TableName, @IndexName

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT @TableName + ':' + @IndexName

    SET @sql = REPLACE(@basesql, '@1', @IndexName)
    SET @sql = REPLACE(@sql, '@2', @TableName)
   
    EXECUTE (@sql)

    FETCH NEXT FROM IXC
    INTO @TableName, @IndexName   
END

CLOSE IXC
DEALLOCATE IXC
```
