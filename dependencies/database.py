from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling


class DatabaseWrapper:

    connection = None
    def __init__(self, connection):
        self.connection = connection
    
    def registration(self,username,password):
        cursor=self.connection.cursor(dictionary=True,buffered=True)
        result=[]
        sql="SELECT * FROM user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount>0):
            cursor.close()
            result.append("Existed")
            return result
        else:
            sql = "INSERT INTO user VALUES(0,'{}', '{}')".format(username, password)
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            result.append("Registrasi Complete")
            return result

    def login(self, username, password):
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        result = []
        sql = "SELECT * FROM user where username = '{}'".format(username)
        cursor.execute(sql)
        if(cursor.rowcount == 0):
            cursor.close()
            result.append("User not found")
            return 0
        else:
            resultfetch = cursor.fetchone()
            if(resultfetch['password'] == password):
                cursor.close()
                result.append("Login Berhasil")
                return 1
            else:
                cursor.close()
                result.append("Fail")
                return 0


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='cloud_storage_db',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())