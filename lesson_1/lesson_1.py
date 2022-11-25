# 1. Каждое из слов «разработка», «сокет», «декоратор»
# представить в строковом формате
# и проверить тип и содержание соответствующих переменных.
# Затем с помощью онлайн-конвертера
# преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.

# 2. Каждое из слов «class», «function», «method»
# записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

# 3. Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе.

# 4. Преобразовать слова
# «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).

# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.

# 6. Создать текстовый файл test_file.txt,
# заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

import subprocess
import sys
from chardet.universaldetector import UniversalDetector

def task_1():
    print('строки:')
    str_tpl = ('разработка', 'сокет', 'декоратор')
    # print(tuple(type(i) for i in str_tpl))
    # print(tuple(map(type, str_tpl)))
    for i, j in zip(map(type, str_tpl), str_tpl):
        # print(i, j)
        print(f'тип:{i},\tсодержимое:{j}')

    print('\nбайты:')
    # https://unicode-table.com/ru/tools/decoder/
    byte_tpl = (
        b'\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
        b'\u0441\u043e\u043a\u0435\u0442',
        b'\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
    )
    for i, j in zip(map(type, byte_tpl), byte_tpl):
        print(f'тип:{i},\tсодержимое:{j}')


def task_2():
    str_tpl = ('class', 'function', 'method')
    for i in str_tpl:
        i = bytes(i, 'utf-8')
        print(f'тип:{type(i)},\tсодержимое:{i},\tдлина:{len(i)}')


def task_3():
    str_tpl = ('attribute', 'класс', 'функция', 'type')
    for i in str_tpl:
        try:
            i.encode('ascii')
        except UnicodeEncodeError:
            print(f'«{i}» невозможно записать в байтовом типе (ascii)')


def task_4():
    str_tpl = ('разработка', 'администрирование', 'protocol', 'standard')
    print('из строк в байты:')
    b_list = []
    for i in str_tpl:
        i = str.encode(i, encoding='utf-8')
        b_list.append(i)
        print(i)
    print('\nиз байт в строки:')
    for i in b_list:
        print(bytes.decode(i, encoding='utf-8'))


def task_5(domain: str, c: int = 4):
    print(sys.platform)
    if 'win' in sys.platform:
        args = ['ping', f'{domain}']
        ping_ya = subprocess.run(args, capture_output=True)
        os_coding = sys.getfilesystemencoding()
        print(ping_ya.stdout.decode(os_coding))
    else:
        # в ubuntu команда ping по-умолчанию работает пока не остановишь,
        # поэтому останавливаю после 4 ответов
        args = ['ping', f'-c {c}', f'{domain}']
        ping_ya = subprocess.Popen(args, stdout=subprocess.PIPE)
        for i in ping_ya.stdout:
            print(i.decode('utf-8').replace('\n', ''))
    # не тестировал на Маках (sys.platform='Darwin')
    # (надо сначала найти и скачать образ для виртуалки),
    # но надеюсь, что в POSIX-системах работает


def task_6():
    files = ('test_file.txt', 'test_koi8r.txt', 'test_win.txt')
    detector = UniversalDetector()
    for file in files:
        detector.reset()
        for line in open(file, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        file_encoding = detector.result.get('encoding')
        print(f'\nфайл: {file}\nкодировка:{file_encoding}')
        with open(file, 'r', encoding=file_encoding) as f:
            print('содержимое файла:')
            for row in f:
                print(row)


if __name__ == '__main__':
    print('Задание 1\n')
    task_1()

    print(f'\n{"=" * 45}')
    print('Задание 2\n')
    task_2()

    print(f'\n{"=" * 45}')
    print('Задание 3\n')
    task_3()

    print(f'\n{"=" * 45}')
    print('Задание 4\n')
    task_4()

    print(f'\n{"=" * 45}')
    print('Задание 5')
    for d in ('yandex.ru', 'youtube.com'):
        print('\nпингуем', d)
        task_5(d)

    print(f'\n{"=" * 45}')
    print('Задание 6\n')
    task_6()
