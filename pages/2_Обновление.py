import openpyxl as op
import streamlit as st
import sqlite3 as sq
import os
import pandas as pd

from DB_work import DB_ORM
from streamlit import *
from openpyxl_image_loader import SheetImageLoader



hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

DB_object = DB_ORM()

uploaded_file = st.file_uploader("Загрузите файл - сводку", type = ['xlsx', 'xls'], accept_multiple_files = False)

if uploaded_file is not None:
    # st.code(uploaded_file)
    sheet_name = st.text_input('Введите точное название листа с таблицей')
    # st.code('xl' in uploaded_file.name.split('.')[-1])

    try:
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name if sheet_name else 'Лист2')
        st.write(df)
        insert_ready = True

    except ValueError:
        st.code('Введено несуществующее имя листа')
        insert_ready = False

    

    if st.button('Загрузить', disabled = not insert_ready):
        query = ''
        quote = "'"
        quotes = '"'

        df.dropna(inplace = True)
        df.drop_duplicates(inplace = True)

        # st.code(df.columns)

        # with open("Pics/no_pic_provided.png", 'rb') as no_image_provided:
        #     # DB_object.execute(query = "INSERT INTO ФОТО (id, Изображение) VALUES (0, ?)", is_change = True, values = (bin_png.read(),))
        #     no_image_provided = no_image_provided.read()

        no_image_provided = True
        


        for row_counter in range(len(df)):
            row = df.iloc[row_counter].to_dict()
            # st.write(row)


            try:
                # DB_object.execute(f"""INSERT INTO {DB_name} ({insertion_column}) VALUES ({quotes + value.replace(quotes, '``') + quotes});""", is_change=True)
                # query = "INSERT INTO СВОДКА VALUES (" + ', '.join([DB_object.names[key] for key in row.keys()]) + ");"
                is_exists  = {}

                for column_name in row.keys():
                    table_name = DB_object.names[column_name]
                    # st.write(column_name, table_name, row[column_name])
                    # st.code(DB_object.execute(f'SELECT id from {table_name} WHERE {DB_object.columns_names(table_name)[1]} = ' + "'" + row[column_name] + "'", is_change=False))
                    find = DB_object.execute(f'SELECT id from {table_name} WHERE {DB_object.columns_names(table_name)[1]} = ' + "'" + row[column_name].replace("'", "`") + "'", is_change=False)

                    if find != []:
                        is_exists.update({column_name : find[0][0]})
                    
                    else:
                        DB_object.execute(f"INSERT INTO {table_name} ({DB_object.columns_names(table_name)[1]}) VALUES ('" + row[column_name].replace("'", "`") + "')", is_change = True)
                        
                        upd = {column_name : DB_object.execute(f'SELECT id from {table_name} WHERE {DB_object.columns_names(table_name)[1]} = ' + "'" + row[column_name].replace("'", "`") + "'", is_change=False)[0][0]}
                        is_exists.update(upd)

                # st.code(is_exists)
                if no_image_provided:
                    # st.code([is_exists[key] for key in row.keys()])
                    query = "INSERT INTO СВОДКА VALUES (" + ', '.join([str(is_exists[key]) for key in row.keys()]) + f", 0);"   # TODO: Додумать запись картинок
                
                else:
                    ...

                st.code(query)
                DB_object.execute(query, is_change=True)

            except sq.IntegrityError as e:
                if 'UNIQUE constraint failed' in str(e):
                    pass

                else:
                    raise e

        # for df_column in list(df.columns):
        #     DB_name = DB_object.names[df_column]
        #     insertion_column = DB_object.columns_names(DB_name)[1]

        #     for value in df[df_column].unique():
        #         try:
        #             # DB_object.execute(f"""INSERT INTO {DB_name} ({insertion_column}) VALUES ({quotes + value.replace(quotes, '``') + quotes});""", is_change=True)
        #             DB_object.execute(f"""INSERT INTO СВОДКА VALUES ({})""")


        #         except sq.IntegrityError as e:
        #             if 'UNIQUE constraint failed' in str(e):
        #                 pass

        #             else:
        #                 raise e

        st.code('Execution completed!')

