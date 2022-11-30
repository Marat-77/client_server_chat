# 3. Задание на закрепление знаний по модулю yaml.
# Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
# Для этого:
# Подготовить данные для записи в виде словаря,
# в котором первому ключу соответствует список,
# второму — целое число,
# третьему — вложенный словарь,
# где значение каждого ключа — это целое число с юникод-символом,
# отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например,
# в файл file.yaml.
# При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
# а также установить возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить,
# совпадают ли они с исходными.

import yaml


def myaml():
    yml_file = 'file.yaml'
    data = {
        'first': ['winter', 'spring', 'summer', 'autumn'],
        'second': 15,
        'third': {
            'RUB': '₽',
            'CNY': '元',
            'INR': '₹',
            'EUR': '€'
        }
    }
    print(data)
    with open(yml_file, 'w') as fd:
        # При этом обеспечить стилизацию файла с помощью параметра
        # default_flow_style,
        # а также установить возможность работы с юникодом:
        # allow_unicode = True;
        yaml.dump(data, fd, default_flow_style=False, allow_unicode=True)

    with open(yml_file) as fd:
        result = yaml.load(fd, Loader=yaml.FullLoader)
        print(result)
    if data == result:
        print('Полученные данные совпадают с исходными')


if __name__ == '__main__':
    myaml()
