from psycopg2 import pool

class Database:
    connection_pool = None
    
    @classmethod
    def initialise(cls):
        cls.connection_pool = pool.SimpleConnectionPool(1, 1, database='finisher', user='finisher', password='aston2018', host='localhost')
    
    @classmethod
    def get_connection(cls):
        return cls.connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, connection):
        Database.connection_pool.putconn(connection)

class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor=None
    
    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_traceback is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)