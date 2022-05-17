import mysql.connector
import yaml

class MySQLConn():
    def __init__(self):
        with open("cgi-bin/config.yaml", "r") as config:
            cfg = yaml.safe_load(config)
        self._dbhost = cfg['mysql']['host']
        self._dbuser = cfg['mysql']['user']
        self._dbpassword = cfg['mysql']['password']
        self._dbname = cfg['mysql']['database']
        self._dbcharset = 'utf8'
        self._dbport = int(3306)
        self.conn = self.connect_db()
        self.cursor = None

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host=self._dbhost,
                user=self._dbuser,
                passwd=self._dbpassword,
                db=self._dbname,
                port=self._dbport,
                charset=self._dbcharset)
        except Exception as e:
            print("数据库连接出错")
            conn = False
        return self.conn

    def get_cursor(self):
        if self.conn:
            self.cursor = self.conn.cursor()
        return self.cursor

if __name__ == '__main__':
    pass
    # db_conn = MySQLConn()
    # cursor = db_conn.get_cursor()
    # cursor.execute("SELECT * FROM user")
    # result = cursor.fetchall()
    # print(result)