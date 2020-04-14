import os
import mysql.connector
import contextlib
from constants import DEFAULT_DB_HOST, DEFAULT_DB_PORT

class DBConn(object):
    """
    DBConnection class for handling context manager.
    To use this kindly follow these steps:
    1. Instantiate an object of the class: obj = DBConn()
    2. If you want, you can set the host and the port throught the init but it will automatically pick it up from your environments
    3. Run insert_query for DML or get_query for DQL (Select statements)
    4. Context and connections are handled in execute_statement. This will terminate it as the query finishes.
    """
    def __init__(self, host=os.environ.get('DB_HOST', DEFAULT_DB_HOST),
                        port=os.environ.get('DB_PORT', DEFAULT_DB_PORT)):
        self.host = host
        self.port = int(port)
        self.connection = None

    def create_connection(self, save_to_self=False):
        """
        Sets up a connection and returns it based on the environment variables
        """
        try:
            conn = mysql.connector.connect(host=self.host,
                    port=self.port,
                    user=os.environ.get('DB_ROOT', 'root'),
                    password=os.environ.get('DB_PASSWORD', ''))
            if save_to_self:
                self.connection = conn

            return conn
        except Exception as exc:
            print(exc)

    def multi_statement_exec(self, executed):
        final_result = []
        try:
            for result in executed:
                if result.with_rows:
                    print(f"Rows produced by statement '{result.statement}':")
                    final_result.append(result.fetchall())
                else:
                    print(f"Number of rows affected by statement '{result.statement}': {result.rowcount}")
        except RuntimeError as exc:
            # To handle stop iteration
            # Changed in version 3.7: Enable PEP 479 for all code by default: a StopIteration error raised in a generator is transformed into a RuntimeError.
            pass
        return final_result

    def execute_statement(self, statement:str, return_val:bool=False, commit:bool=False, execute_many:bool=False):
        """
        Creates a context manager and manages all connections.
        It also closes this after the cursor has been executed
        """
        with contextlib.closing(self.connection if self.connection else self.create_connection()) as conn: # auto-closes
            with contextlib.closing(conn.cursor()) as cursor: # auto-closes
                executed = cursor.execute(statement, multi=execute_many)
                # If its an insert then we need to commit
                if commit:
                    conn.commit()
                # If its a get it needs to return and based on multi statement responses we have to handle operations accordingly
                if return_val:
                    return cursor.fetchall() if not execute_many else self.multi_statement_exec(executed)


    def insert_query(self, query):
        """
        Should be used for inserting
        """
        self.execute_statement(query, commit=True)


    def get_query(self, query:str, execute_many:bool=False):
        """
        Should be used as a get query
        """
        return self.execute_statement(query, return_val=True, execute_many=execute_many)


# if __name__ == '__main__':
#     obj = DBConn()
#     print(obj.get_query('select 1+1; select 4;', True))
#     print(obj.get_query('select 1+4;', False))

#     print(obj.get_query('show processlist'))




