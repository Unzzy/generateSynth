import pandas as pd
import time
import generators

glossary_table_name = input("Введите название таблицы:\n")
glossary_row_count = int(input('Введите количество атрибутов таблицы\n'))
print("Вставьте поля из глоссария ИМЯ - ТИП - КОЛИЧЕСТВО СИМВОЛОВ разовой вставкой")
table_arr = [[0] * 3 for _ in range(glossary_row_count)]  # создание пустого массива
a = [i for i in iter(input, '')]  # чтение параметров таблицы


dataset_row_count = 1000
start_time = time.time()
primary_keys = pd.read_csv('keys.csv')  # чтение Primary keys из csv файла
pk_flag = False
list_of_columns_pk = primary_keys.columns

for i in range(glossary_row_count):  # запись параметров в массив
    if len(a[i].split()) == 3:
        table_arr[i][0], table_arr[i][1], table_arr[i][2] = a[i].split()
    else:
        table_arr[i][0], table_arr[i][1] = a[i].split()
df = pd.DataFrame()
format_date = '%Y-%m-%d 00:00:00.000'
for i in range(glossary_row_count):
    name = table_arr[i][0]
    column_name_split = name.split('_')  # разбивка имени поля для определения интервала даты и поиска GID
    values = []

    if table_arr[i][1] == 'NUMBER' and 'GID' in column_name_split:
        name_gid = f'{column_name_split[-2]}_{column_name_split[-1]}'
        if name_gid not in list_of_columns_pk:
            for _ in range(dataset_row_count):
                values.append(generators.number_generate(99999999, 999999999))
            df[name] = values
            primary_keys[name_gid] = values
            pk_flag = True
        elif name_gid in list_of_columns_pk:
            for _ in range(dataset_row_count):
                values.append(primary_keys.iloc[generators.number_generate(1, 999)][name_gid])
            df[name] = values

    elif table_arr[i][1] == 'VARCHAR2':
        length_varchar = int(table_arr[i][2])
        for _ in range(dataset_row_count):
            values.append(generators.string_generate(2, length_varchar, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"))
        df[name] = values

    elif table_arr[i][1] == 'CHAR' and "STATUS" in column_name_split:
        for _ in range(dataset_row_count):
            values.append(generators.string_generate(1, 1, "AD"))
        df[name] = values

    elif table_arr[i][1] == 'CHAR' and "FLG" in column_name_split:
        for _ in range(dataset_row_count):
            values.append(generators.string_generate(1, 1, "YN"))
        df[name] = values

    elif table_arr[i][1] == 'DATE' and ("START" in column_name_split or "BEGIN" in column_name_split):
        begin_date = '2015-01-01 00:00:00.000'
        end_date = '2018-12-31 00:00:00.000'
        for _ in range(dataset_row_count):
            values.append(generators.date_generate(begin_date, end_date, format_date))
        df[name] = values

    elif table_arr[i][1] == 'DATE' and ("END" in column_name_split or "CHANGE" in column_name_split):
        begin_date = '2019-01-01 00:00:00.000'
        end_date = '2022-12-31 00:00:00.000'
        for _ in range(dataset_row_count):
            values.append(generators.date_generate(begin_date, end_date, format_date))
        df[name] = values

    elif table_arr[i][1] == 'DATE':
        begin_date = '2015-01-01 00:00:00.000'
        end_date = '2022-12-31 00:00:00.000'
        for _ in range(1000):
            values.append(generators.date_generate(begin_date, end_date, format_date))
        df[name] = values
    elif table_arr[i][1] == 'NUMBER':
        for _ in range(dataset_row_count):
            values.append(generators.number_generate(1, 999999999))
        df[name] = values

print(f"Генерация закончена за {time.time() - start_time}")
if pk_flag:
    primary_keys.to_csv('keys.csv', index=False)
df.to_csv(glossary_table_name + '.csv', index=False)
