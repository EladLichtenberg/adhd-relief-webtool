import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = '333879096'
DBNAME = 'adhd_final_project'


class DB:

    def __init__(self, host, db_name, user, password):
        self._host = host
        self._db_name = db_name
        self._user = user
        self._password = password

    def open_connection(self):
        try:
            connection = pymysql.connect(host=self._host,
                                         user=self._user,
                                         password=self._password,
                                         database=self._db_name,
                                         cursorclass=pymysql.cursors.DictCursor)  # noqa
        except pymysql.MySQLError as e:
            print(e)
            return None
        return connection

    def execute_query(self, query):
        try:
            conn = self.open_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            conn.close()
            return result
        except pymysql.MySQLError as e:
            print(e)
            return None


db = DB(HOST, DBNAME, USER, PASSWORD)


# def fetch(query):
#     # query = f"SELECT * FROM Users WHERE email='{email}'"
#     req = query.split(sep='\'')
#     result = req[1]
#     for x in USERS_TABLE:
#         if x['email'] == result:
#             return x
#     return None

if __name__ == '__main__':
    email = 'docmat63@gmail.com'
    query = f"SELECT * FROM Users WHERE email='{email}'"
    e = db.execute_query(query)
    print(e)


