import sqlite3 as sq
import os 
import json

class DB_ORM:
    def __init__(self, db_name : str):
        self.__connect(db_name)
        self.names = {
            'Здание' : 'ЗДАНИЯ', 
            'Помещение' : "ПОМЕЩЕНИЯ", 
            "Машина" : "МАШИНЫ", 
            "Адрес" : "АДРЕСА", 
            "Системы" : "СИСТЕМЫ", 
            "Оборудование" : "ОБОРУДОВАНИЕ",
            "Фото" : "ФОТО"
        }


    def __connect(self, db_name):
        os.mkdir('DBs') if not os.path.exists('DBs') else ...
        self.connection = sq.connect(f"DBs/{db_name}.db")
        self.cursor = self.connection.cursor()

        # Создание таблицы зданий
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS ЗДАНИЯ (
            id INTEGER PRIMARY KEY, 
            'Наименование' varchar NOT NULL,
            UNIQUE('Наименование')
        )
        """, 
        is_change=True)

        # Создание таблицы помещений
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS ПОМЕЩЕНИЯ (
            id INTEGER PRIMARY KEY, 
            'Номер' varchar  NOT NULL,
            UNIQUE('Номер')
        )
        """, 
        is_change=True)

        # Создание таблицы "машин"
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS МАШИНЫ (
            id INTEGER PRIMARY KEY, 
            'Наименование' varchar  NOT NULL,
            UNIQUE('Наименование')
        )
        """, 
        is_change=True)

        # Создание таблицы устройств
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS СИСТЕМЫ (
            id INTEGER PRIMARY KEY, 
            'Наименование' varchar  NOT NULL,
            UNIQUE('Наименование')
        )
        """, 
        is_change=True)

        # Создание таблицы оборудования
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS ОБОРУДОВАНИЕ (
            id INTEGER PRIMARY KEY, 
            'Наименование' varchar  NOT NULL,
            UNIQUE('Наименование')
        )
        """, 
        is_change=True)

        # Создание таблицы адресов
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS АДРЕСА (
            id INTEGER PRIMARY KEY, 
            'Адрес' varchar(256)  NOT NULL,
            UNIQUE ('Адрес')
        )
        """, 
        is_change=True)

        # Создание таблицы фоток. Лучше использовать БД, поскольку отпадает проблема одновременного доступа к одному и тому же файлу.
        self.execute(f"""
        CREATE TABLE IF NOT EXISTS ФОТО (
            id INTEGER PRIMARY KEY, 
            'Изображение' BLOB  NOT NULL,
            UNIQUE ('Изображение')
        )
        """, 
        is_change=True)

        # Создание таблицы-сводки
        self.execute("""
        CREATE TABLE IF NOT EXISTS СВОДКА (
            Здание INTEGER NOT NULL,
            Помещение INTEGER NOT NULL,
            Машина INTEGER NOT NULL,
            Адрес INTEGER NOT NULL,
            Системы INTEGER NOT NULL,
            Оборудование INTEGER NOT NULL,
            Фото INTEGER NOT NULL
        )

        """,
        is_change=True)


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