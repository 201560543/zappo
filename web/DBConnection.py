import os
import mysql.connector
import contextlib

class DBConn(object):
    """
    DBConnection class for handling context manager.
    """
    def __init__(self, host=os.environ.get('DB_HOST', 'localhost'),
                        port=os.environ.get('DB_PORT', 3306)):
        self.host = host
        self.port = int(port)
        self.connection = None

    def create_connection(self):
        """
        Sets up a connection and returns it based on the environment variables
        """
        try:
            return mysql.connector.connect(host=self.host,
                    port=self.port,
                    user=os.environ.get('DB_ROOT', 'root'),
                    password=os.environ.get('DB_PASSWORD', ''))
        except Exception as exc:
            print(exc)


    def execute_statement(self, statement:str, return_val:bool=False, commit:bool=False):
        """
        Creates a context manager and manages all connections.
        It also closes this after the cursor has been executed
        """
        with contextlib.closing(self.create_connection()) as conn: # auto-closes
            with contextlib.closing(conn.cursor()) as cursor: # auto-closes
                cursor.execute(statement)
                if commit:
                    conn.commit()
                if return_val:
                    result = cursor.fetchall()

        return result


    def insert_query(self, query):
        """
        Should be used for inserting
        """
        self.execute_statement(query)


    def get_query(self, query):
        """
        Should be used as a get query
        """
        return self.execute_statement(query, return_val=True)


