import sqlite3 as sq
import os 
import json

class DB_ORM:
    def __init__(self):
        self.__connect()
        self.names = {
            'Здание' : 'ЗДАНИЯ', 
            'Помещение' : "ПОМЕЩЕНИЯ", 
            "Машина" : "МАШИНЫ", 
            "Адрес" : "АДРЕСА", 
            "Системы" : "СИСТЕМЫ", 
            "Оборудование" : "ОБОРУДОВАНИЕ",
            "Фото" : "ФОТО"
        }

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
        self.connection = sq.connect("DBs/multi_test.db")
        self.cursor = self.connection.cursor()

        # self.connection = sq.connect("DBs/TESTS.db")
        # self.cursor = self.connection.cursor()

        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS test_table (
        #     Здание varchar(512),
        #     Помещение varchar(512),
        #     Машина varchar(512),
        #     Адрес varchar(512),
        #     Системы varchar(512),
        #     Оборудование varchar(512),
        #     Фото BLOB
        #     )''')
        # self.connection.commit()

    def dict_reverse_search(self, dictionary : dict, search_value : str):
        return(list(dictionary.keys())[list(dictionary.values()).index(search_value)] if search_value in list(dictionary.values()) else False)

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

    def get_unique(self, table_name : str, dictionary : dict) -> list:
        # self.cursor.execute(f'SELECT DISTINCT {column} FROM {table_name}')
        # return([item[0] for item in self.cursor.fetchall()])

        if self.connection_check():
            return([x[0] for x in self.execute(f"""
        SELECT DISTINCT {table_name}.{self.columns_names(table_name)[1]} FROM 
            {table_name} JOIN {'СВОДКА'} 
                ON {table_name}.id = {'СВОДКА'}.{self.dict_reverse_search(dictionary, table_name)}
        """, 
        is_change=False)])      # Непонятки с первым элементом, получаемым таким запросом. Разобраться. 

        else:
            print('Have no connection to database')
    
    def connection_check(self):
        try:
            self.cursor.execute('SELECT 1;')
            return True

        except Exception:
            return False

    def columns_names(self, table_name : str) -> list:
        return([name[1] for name in self.execute(f'''PRAGMA table_info({table_name});''', is_change = False)])

    def connection_close(self):
        self.connection.close()