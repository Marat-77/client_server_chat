# 1. Задание на закрепление знаний по модулю CSV.
# Написать скрипт, осуществляющий выборку определенных данных из файлов
# info_1.txt, info_2.txt, info_3.txt
# и формирующий новый «отчетный» файл в формате CSV.
# Для этого:
# Создать функцию get_data(),
# в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных.
# В этой функции из считанных данных необходимо
# с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например,
# os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета
# — например, main_data
# — и поместить в него названия столбцов отчета в виде списка:
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка
# и поместить в файл main_data (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
# В этой функции реализовать получение данных через вызов функции get_data(),
# а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().

import re
import csv


def get_data():
    # в которой в цикле осуществляется перебор файлов с данными,
    # их открытие и считывание данных.
    # «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
    headers = ['Изготовитель системы',
               'Название ОС',
               'Код продукта',
               'Тип системы']
    main_data = [headers]
    os_prod_list = list()
    os_name_list = list()
    os_code_list = list()
    os_type_list = list()
    patterns = {
        'os_prod': re.compile(r'^Изготовитель системы:\s+(?P<os_prod>.+)$'),
        'os_name': re.compile(r'^Название ОС:\s+(?P<os_name>.+)$'),
        'os_code': re.compile(r'^Код продукта:\s+(?P<os_code>.+)$'),
        'os_type': re.compile(r'^Тип системы:\s+(?P<os_type>.+)$'),
    }
    files = ('info_1.txt', 'info_2.txt', 'info_3.txt')
    for file in files:
        line_count = 0
        with open(file, 'r', encoding='cp1251') as fd:
            for f_line in fd:
                if patterns['os_prod'].search(f_line):
                    os_prod_list.append(
                        patterns['os_prod'].search(f_line).group('os_prod')
                    )
                    line_count += 1
                elif patterns['os_name'].search(f_line):
                    os_name_list.append(
                        patterns['os_name'].search(f_line).group('os_name')
                    )
                    line_count += 1
                elif patterns['os_code'].search(f_line):
                    os_code_list.append(
                        patterns['os_code'].search(f_line).group('os_code')
                    )
                    line_count += 1
                elif patterns['os_type'].search(f_line):
                    os_type_list.append(
                        patterns['os_type'].search(f_line).group('os_type')
                    )
                    line_count += 1

                if line_count == len(patterns):
                    # нашли всё, что искали - нет смысла продолжать цикл
                    break
    for os_prod, os_name, os_code, os_type in zip(os_prod_list,
                                                  os_name_list,
                                                  os_code_list,
                                                  os_type_list):
        main_data.append([os_prod, os_name, os_code, os_type])
    return main_data


def write_to_csv(f):
    # в которую передавать ссылку на CSV-файл
    # реализовать получение данных через вызов функции get_data(),
    # а также сохранение подготовленных данных в соответствующий CSV-файл;
    data = get_data()
    with open(f, 'w') as fd:
        writer = csv.writer(fd)
        writer.writerows(data)


def main():
    file_path = 'info.csv'
    write_to_csv(file_path)


if __name__ == '__main__':
    main()
