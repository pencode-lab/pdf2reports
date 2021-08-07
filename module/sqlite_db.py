import sqlite3 as lite

class HandleSqlite:
    def __init__(self, db_file):

        self.data = db_file 

    def conn_sqlite(self):
        """连接数据库"""
        self.conn = lite.connect(self.data)
        self.cur = self.conn.cursor()

    def execute_sql(self, sql, data):
        """执行操作数据的相关sql"""
        self.conn_sqlite()
        self.cur.execute(sql,data)
        self.conn.commit()

    def search(self, sql):
        """执行查询sql"""
        self.conn_sqlite()
        self.cur.execute(sql)
        return self.cur.fetchall()




    def close_sqlite(self):
        """关闭数据库连接"""
        self.cur.close()
        self.conn.close()

