import openpyxl as op
import streamlit as st
import sqlite3 as sq
import os
import pandas as pd

from DB_work import DB_ORM
from streamlit import *
from openpyxl_image_loader import SheetImageLoader

table_path = 'K:\Downloads\Загрузки Яндекс\Прототип.xlsx'
DB_object = DB_ORM()
hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#loading the Excel File and the sheet
xl_file = op.load_workbook(filename = table_path,  data_only = True)
working_sheet = xl_file[xl_file.sheetnames[1]]      # 0 - Пикча, 1 - таблица

# st.write(DB_object.execute('SELECT * FROM test_table', is_change=False)[: 50])
def state_upd(name : str, val : str) -> None:
    vals = st.session_state[name]
    vals.remove(val)
    vals.insert(0, val)

    st.session_state.update({name : vals})

st.session_state.update({
    'building_select' : ['Не важно'] + DB_object.get_unique('Наименование', 'ЗДАНИЯ'),
    'room_select' : '',
    'machine_select' : ['Не важно'] + DB_object.get_unique('Наименование', "МАШИНЫ"),
    'address_select' : '',
    'system_select' : ['Не важно'] + DB_object.get_unique('Наименование', "СИСТЕМЫ"),
    'equipping_select' : ''
})

with open('is_help.txt', 'r') as help_file:
    st.session_state.is_help = help_file.read()


if st.session_state.is_help == '1':
    help_text_layout = st.empty()
    help_button_layout = st.empty()
    # help_text = help_text_layout.text_area('Подсказка', 'В любом поле для ввода вы можете указать любой аргумент - в базе данных будут искаться записи, содержащие введенные вами аргументы. Поля с выпадающими списками содержат значения из базы данных.', disabled=True)
    help_text = help_text_layout.write('''1. В любом поле для ввода вы можете указать любой аргумент - в базе данных будут искаться записи, содержащие введенные вами аргументы. \n\n2. Поля с выпадающими списками содержат значения из базы данных.''')


    help_button = help_button_layout.button('Убрать подсказку', key = 'help_button')

    if help_button:
        help_button_layout.empty()
        help_text_layout.empty()
        st.session_state.is_help = 0
        with open('is_help.txt', 'w') as help_file:
            help_file.write('0')


left_column, right_column = st.columns(2)

with left_column:
    building_select = st.selectbox(label = 'Здание', options = st.session_state.building_select)
    # building_select = st.text_input(label = 'Здание', label_visibility = 'visible', placeholder='Введите наименование здания')

    room_select = st.text_input(label = 'Помещение', label_visibility = 'visible', placeholder='Введите наименование помещения (опц.)', value = st.session_state.room_select)

    # machine_select = st.text_input(label = 'Машина', label_visibility = 'visible', placeholder='Введите наименование машины (опц.)')
    machine_select = st.selectbox(label = 'Машина', label_visibility = 'visible', options = st.session_state.machine_select)
    


with right_column:
    address_select = st.text_input(label = 'Адрес', label_visibility = 'visible', placeholder='Введите адрес устройства (опц.)')

    system_select = st.selectbox(label = 'Системы', label_visibility = 'visible', options = st.session_state.system_select)
    # system_select = st.text_input(label = 'Системы', label_visibility = 'visible', placeholder='Введите имя системы (опц.)')

    equipping_select = st.text_input(label = 'Оборудование', label_visibility = 'visible', placeholder='Введите оборудование устройства (опц.)')

    # address_select = st.text_input(label = 'Адрес', label_visibility = 'visible', placeholder='Введите адрес устройства (опц.)')

if st.button('Поиск'):
    state_upd('building_select', building_select)
    state_upd('machine_select', machine_select)
    state_upd('system_select', system_select)

    quote = '"'
    quote_one = "'"

    query = f'''
    SELECT * FROM test_table WHERE (
        {str(quote + "Здание" + quote) if building_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{building_select}%{quote_one} AND") if building_select != "Не важно" else ''} 
        {str(quote + "Машина" + quote) if machine_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{machine_select}%{quote_one} AND") if machine_select != "Не важно" else ''} 
        {str(quote + "Системы" + quote) if system_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{system_select}%{quote_one} AND") if system_select != "Не важно" else ''}
        {str(quote + "Помещение" + quote) if room_select != "" else ''}{str(f" LIKE {quote_one}%{room_select}%{quote_one} AND") if room_select != "" else ''}
        {str(quote + "Адрес" + quote) if address_select != "" else ''}{str(f" LIKE {quote_one}%{address_select}%{quote_one} AND") if address_select != "" else ''}
        {str(quote + "Оборудование" + quote) if equipping_select != "" else ''}{str(f" LIKE {quote_one}%{equipping_select}%{quote_one} AND") if equipping_select != "" else ''}
        1
    )
    '''

    response = DB_object.execute(query = query, is_change = False)

    



    a = []
    b = {}
    for row in response:
        for counter, element in enumerate(row):
            b.update({ DB_object.columns_names()[counter] : element })
        
        a.append(b)
        b = {}

    #st.text_area(label = 'Результаты поиска', value = a, disabled = True)


    # for resp_piece in response:
    #     pictures = os.listdir(path = 'cache_pics')
    #     file_type = f'{"png" if "PNG" in resp_piece[-1] else "jpg"}'

    #     if resp_piece[-2] not in [file[ : -4] for file in pictures] and resp_piece[-1] is not None:     # Для срабатывания условия необходима строка, содержащая лишь точное название прибора ( Не "извещатель пожарный ИО 102-6", а просто "ИО 102-6")
    #         with open(f'cache_pics/{resp_piece[-2]}.{file_type}', 'wb') as pic_file:
    #             pic_file.write(bytes(resp_piece[-1]))
            
    #         # выводим картинку на экран
    #         st.image(bytes(resp_piece[-1]), format="jpeg" if file_type == 'jpg' else file_type)
        
    #     elif resp_piece[-1] is not None:
    #         pic_type = file_type if file_type == 'png' else 'JPEG'
    #         st.image(bytes(resp_piece[-1]), format=pic_type)
    st.write(f'Найдено записей : {len(response)}')
    for resp_piece in response:
        # if resp_piece[-1] is not None:
        #     columns = DB_object.columns_names()
        #     for counter, data in enumerate(resp_piece[: -1]):
        #         #st.write(f'''{columns[counter]}: {data}''')
        #         st.write(f'''<u>{columns[counter]}: {data}</u>''', unsafe_allow_html=True)
            
        #     st.write(str("<ul>" + '\n'.join([f'''<li>{DB_object.columns_names()[counter]}: {data}''' for resp_piece in response for counter, data in enumerate(resp_piece[: -1])]) + "</ul>")  if resp_piece[-1] is not None else 'Изображение не найдено', unsafe_allow_html=True)

        #     st.image(bytes(resp_piece[-1]))
        
        # else:
        #     st.write('Изображение не нвйдено')


        # Отображаем таблицу в Streamlit
        # st.write([ { : data} for counter, data in enumerate(resp_piece[: -1])])
        # st.write([{DB_object.columns_names()[counter] : data} for counter, data in enumerate(resp_piece[: -1])]  if resp_piece[-1] is not None else 'Изображение не найдено')
        # st.table(pd.DataFrame({DB_object.columns_names()[counter] : data} for counter, data in enumerate(resp_piece[: -1]))  if resp_piece[-1] is not None else 'Изображение не найдено')
        # st.write(str("<ul>" + '\n'.join([f'''<li>{DB_object.columns_names()[counter]}: {data}'''  for counter, data in enumerate(resp_piece[: -1])]) + "</ul>")  if resp_piece[-1] is not None else 'Изображение не найдено', unsafe_allow_html=True)

        aboba = {}
        for counter, data in enumerate(resp_piece[: -1]):
            aboba.update({ DB_object.columns_names()[counter] : data })
        
        st.write(pd.DataFrame.from_dict(aboba, orient='index').T)

        # st.table(pd.DataFrame(aboba))



        st.image(bytes(resp_piece[-1]))

        for i in range(2):
            st.write("<hr size='5'>", unsafe_allow_html=True)