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
