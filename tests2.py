import openpyxl as op
import streamlit as st
import sqlite3 as sq
import os
import pandas as pd

from DB_work import DB_ORM
from streamlit import *
from openpyxl_image_loader import SheetImageLoader

# table_path = 'K:\Downloads\Загрузки Яндекс\Прототип.xlsx'
DB_object = DB_ORM()
hide_streamlit_style = """
<style>
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# #loading the Excel File and the sheet
# xl_file = op.load_workbook(filename = table_path,  data_only = True)
# working_sheet = xl_file[xl_file.sheetnames[1]]      # 0 - Пикча, 1 - таблица

# st.write(DB_object.execute('SELECT * FROM test_table', is_change=False)[: 50])
def state_upd(name : str, val : str) -> None:
    vals = st.session_state[name]
    vals.remove(val)
    vals.insert(0, val)

    st.session_state.update({name : vals})

st.session_state.update({
    'building_select' : ['Не важно'] + DB_object.get_unique('ЗДАНИЯ', DB_object.names),
    'room_select' : '',
    'machine_select' : ['Не важно'] + DB_object.get_unique("МАШИНЫ", DB_object.names),
    'address_select' : '',
    'system_select' : ['Не важно'] + DB_object.get_unique( "СИСТЕМЫ", DB_object.names),
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
    building_select = st.selectbox(label = 'Здание', label_visibility = 'visible', options = st.session_state.building_select)

    system_select = st.selectbox(label = 'Системы', label_visibility = 'visible', options = st.session_state.system_select)

    machine_select = st.selectbox(label = 'Машина', label_visibility = 'visible', options = st.session_state.machine_select)
    


with right_column:
    address_select = st.text_input(label = 'Адрес', label_visibility = 'visible', placeholder='Введите адрес устройства (опц.)')
    
    room_select = st.text_input(label = 'Помещение', label_visibility = 'visible', placeholder='Введите наименование помещения (опц.)', value = st.session_state.room_select)

    equipping_select = st.text_input(label = 'Оборудование', label_visibility = 'visible', placeholder='Введите оборудование устройства (опц.)')


if st.button('Поиск'):
    state_upd('building_select', building_select)
    state_upd('machine_select', machine_select)
    state_upd('system_select', system_select)

    quote = '"'
    quote_one = "'"

    # query = f'''
    # SELECT * FROM test_table WHERE (
        # {str(quote + "Здание" + quote) if building_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{building_select}%{quote_one} AND") if building_select != "Не важно" else ''} 
        # {str(quote + "Машина" + quote) if machine_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{machine_select}%{quote_one} AND") if machine_select != "Не важно" else ''} 
        # {str(quote + "Системы" + quote) if system_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{system_select}%{quote_one} AND") if system_select != "Не важно" else ''}
        # {str(quote + "Помещение" + quote) if room_select != "" else ''}{str(f" LIKE {quote_one}%{room_select}%{quote_one} AND") if room_select != "" else ''}
        # {str(quote + "Адрес" + quote) if address_select != "" else ''}{str(f" LIKE {quote_one}%{address_select}%{quote_one} AND") if address_select != "" else ''}
        # {str(quote + "Оборудование" + quote) if equipping_select != "" else ''}{str(f" LIKE {quote_one}%{equipping_select}%{quote_one} AND") if equipping_select != "" else ''}
        # 1
    # )
    # '''

    query = f'''
        SELECT ЗДАНИЯ.Наименование, ПОМЕЩЕНИЯ.Номер, МАШИНЫ.Наименование, АДРЕСА.Адрес, СИСТЕМЫ.Наименование, ОБОРУДОВАНИЕ.Наименование, ФОТО.Изображение
            FROM 
                AMALGAM JOIN ЗДАНИЯ ON AMALGAM.Здание = ЗДАНИЯ.id
                JOIN ПОМЕЩЕНИЯ ON AMALGAM.Помещение = ПОМЕЩЕНИЯ.id
                JOIN МАШИНЫ ON AMALGAM.Машина = МАШИНЫ.id
                JOIN АДРЕСА ON AMALGAM.Адрес = АДРЕСА.id
                JOIN СИСТЕМЫ ON AMALGAM.Системы = СИСТЕМЫ.id
                JOIN ОБОРУДОВАНИЕ ON AMALGAM.Оборудование = ОБОРУДОВАНИЕ.id
                JOIN ФОТО ON AMALGAM.Фото = ФОТО.id
            WHERE 
                {str(DB_object.names["Здание"] + '.' + DB_object.columns_names(DB_object.names["Здание"])[1]) if building_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{building_select}%{quote_one} AND") if building_select != "Не важно" else ''} 
                {str(DB_object.names["Машина"] + '.' + DB_object.columns_names(DB_object.names["Машина"])[1]) if machine_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{machine_select}%{quote_one} AND") if machine_select != "Не важно" else ''} 
                {str(DB_object.names["Системы"] + '.' + DB_object.columns_names(DB_object.names["Системы"])[1]) if system_select != "Не важно" else ''}{str(f" LIKE {quote_one}%{system_select}%{quote_one} AND") if system_select != "Не важно" else ''}
                {str(DB_object.names["Помещение"] + '.' + DB_object.columns_names(DB_object.names["Помещение"])[1]) if room_select != "" else ''}{str(f" LIKE {quote_one}%{room_select}%{quote_one} AND") if room_select != "" else ''}
                {str(DB_object.names["Адрес"] + '.' + DB_object.columns_names(DB_object.names["Адрес"])[1]) if address_select != "" else ''}{str(f" LIKE {quote_one}%{address_select}%{quote_one} AND") if address_select != "" else ''}
                {str(DB_object.names["Оборудование"] + '.' + DB_object.columns_names(DB_object.names["Оборудование"])[1]) if equipping_select != "" else ''}{str(f" LIKE {quote_one}%{equipping_select}%{quote_one} AND") if equipping_select != "" else ''}
                1;
                '''     # Дописать так, чтобы не формировать огромную таблицу и из нее вычленять что-то нужное, а таким образом, чтобы на этапе джоинов отсеивались ненужные данные

    response = DB_object.execute(query = query, is_change = False)

    st.write(f'Найдено записей : {len(response)}')

    for row in response:
        row_dict = {}

        for counter in range(len(row) - 1):
            row_dict.update({ list(DB_object.names.keys())[counter] : str(row[counter])})
        
        st.write(pd.DataFrame.from_dict(row_dict, 'index').T)
        st.code("\n".join([list(DB_object.names.keys())[counter] + " : " + str(row[counter]) for counter in range(len(row) -1)]))

        st.image(row[-1])
        st.write('---')