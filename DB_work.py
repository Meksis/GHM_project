import sqlite3 as sq
import os 
import json

class DB_ORM:
    def __init__(self):
        self.__connect()

        # self.execute(query = '''CREATE TABLE IF NOT EXISTS test_table (
        #     Здание varchar(512),
        #     Помещение varchar(512),
        #     Машина varchar(512),
        #     Адрес varchar(512),
        #     Системы varchar(512),
        #     Оборудование varchar(512)
        #     )''', is_change = True)
    
    def __connect(self):
        os.mkdir('DBs') if not os.path.exists('DBs') else ...

        self.connection = sq.connect("DBs/TESTS.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS test_table (
            Здание varchar(512),
            Помещение varchar(512),
            Машина varchar(512),
            Адрес varchar(512),
            Системы varchar(512),
            Оборудование varchar(512),
            Фото BLOB
            )''')
        self.connection.commit()


    def execute(self, query : str, is_change : bool, **values) -> list:
        if self.connection_check():

            if values:
                if list(values.keys())[0] == 'values':
                    self.cursor.execute(query, values['values'])
            else:
                self.cursor.execute(query)
            
            if is_change:
                self.connection.commit()
                return True
            
            else:
                return self.cursor.fetchall()
            
        else:
            print('Have no connection to database')

    def get_unique(self, column : str) -> list:
        self.cursor.execute(f'SELECT DISTINCT {column} FROM test_table')
        return([item[0] for item in self.cursor.fetchall()])
    
    def connection_check(self):
        try:
            self.cursor.execute('SELECT 1;')
            return True

        except Exception:
            return False

    def columns_names(self):
        return([name[1] for name in self.execute('''PRAGMA table_info(test_table);''', is_change = False)])

    def connection_close(self):
        self.connection.close()


