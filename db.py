import pymysql
import os

class DB:

    def __init__(self, host, db_name, user, password):
        self._host = host
        self._db_name = db_name
        self._user = user
        self._password = password

    def open_connection(self):
        """
        Opens a connection to a MySQL database.
        The method attempts to establish a connection to the database using the provided host, user, password,
        database name, and cursor class (pymysql.cursors.DictCursor).
        If an exception of type pymysql.MySQLError occurs during the connection attempt, it is printed, and None is returned.

        Returns:
            The established database connection object, or None if an error occurs.

        """
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
        """
            Executes a SQL query on the database connection.

            Opens a connection to the database, creates a cursor object, and executes the provided query.
            The method fetches all the results, commits the transaction, closes the connection, and returns the results.

            If an exception of type pymysql.MySQLError occurs during the execution, it is printed and None is returned.

            Args:
                query (str): The SQL query to execute.

            Returns:
                The results of the query as a list of dictionaries, or None if an error occurs.
        """
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


#Initialize DB connector
# HOST = '34.165.238.176'
# HOST = '127.0.0.1'
# USER = 'root'
# PASSWORD = '333879096'
# DBNAME = 'adhd_final_project'
#
HOST = os.environ.get("ENV_DB_HOST")
USER = os.environ.get("ENV_DB_USER")
PASSWORD = os.environ.get("ENV_DB_PASS")
DBNAME = os.environ.get("ENV_DB_NAME")
db = DB(HOST, DBNAME, USER, PASSWORD)

