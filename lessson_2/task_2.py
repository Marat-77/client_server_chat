# 2. Задание на закрепление знаний по модулю json.
# Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными.
# Для этого:
# Создать функцию write_order_to_json(),
# в которую передается 5 параметров —
# товар (item),
# количество (quantity),
# цена (price),
# покупатель (buyer),
# дата (date).
#
# Функция должна предусматривать запись данных
# в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json()
# с передачей в нее значений каждого параметра.

import datetime
import json


def write_order_to_json(item, quantity, price, buyer, date):
    json_file = 'orders.json'
    with open(json_file, 'r') as fd:
        orders = json.load(fd)
        # {"orders": []}
    orders['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': f'{date:%d.%m.%Y}',
    })
    with open(json_file, 'w') as fd:
        json.dump(orders, fd, indent=4)


def main():
    order1 = ('Хлеб', 1, 32.3, 'user 1', datetime.date(2022, 7, 15))
    order2 = ('Йогурт', 4, 56.8, 'user 2', datetime.date(2022, 8, 3))
    order3 = ('Хлеб', 1, 32.8, 'user 3', datetime.date(2022, 9, 21))
    order4 = ('Сырок', 8, 24.6, 'user 3', datetime.date(2022, 9, 21))
    orders = order1, order2, order3, order4
    for order in orders:
        write_order_to_json(*order)


if __name__ == '__main__':
    main()
