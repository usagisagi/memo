import mysql.connector


class MySQL:
    def __init__(self, config):
        """
        read時
        df_read = pd.read_sql(sql, mysql.conn)
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_sql.html

        write時
        df2 = pd.DataFrame([['sample3', 'CCC']], columns=['title', 'body'])
        df2.to_sql('articles', con, if_exists='append', index=None)
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html

        :param config: 接続設定を格納した辞書
        """
        self.config = config
        self.conn = None

        if config is not None:
            self.connect()

    def connect(self, config=None):
        """接続する"""
        if config is None:
            config = self.config

        conn = mysql.connector.connect(**config)
        self.conn = conn
        return conn


if __name__ == '__main__':
    pass
