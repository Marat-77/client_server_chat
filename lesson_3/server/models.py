import hashlib
import sqlite3

def create_db():
    db_name = 'users.db'
    con = sqlite3.connect(db_name)

    query = 'CREATE TABLE IF NOT EXISTS "users" '
    query += '("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
    query += '"username" varchar(100) NOT NULL UNIQUE, '
    query += '"password" varchar(128) NOT NULL, '
    query += '"first_name" varchar(155) NULL, '
    query += '"last_name" varchar(155) NULL);'
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()
    return con


def add_user(con: sqlite3.Connection, data: tuple):
    query = 'INSERT INTO "users" (username, password, first_name, last_name) '
    query += 'VALUES (?, ?, ?, ?);'
    cur = con.cursor()
    try:
        cur.execute(query, data)
        con.commit()
    except sqlite3.IntegrityError as err:
        print(err, f'({data} уже существует)')
    finally:
        cur.close()


def add_new_user(con: sqlite3.Connection, data: dict):
    data = (data['username'],
            data['password'],
            data['first_name'],
            data['last_name'])
    query = 'INSERT INTO "users" (username, password, first_name, last_name) '
    query += 'VALUES (?, ?, ?, ?);'
    try:
        with con:
            con.execute(query, data)
    except sqlite3.IntegrityError as err:
        print(err, f'({data[0]} уже существует)')
    finally:
        con.close()


def get_hash_pass(password: str) -> str:
    salt = b'\xf1\xccd7\xf1\x1dz\x8d\\\xa6/\x85\xf8\xb9-\x14\x1e\xed~\xa7\x92\n\x05\xab{$\xb5TD\xf2\xa2<'
    key = hashlib.pbkdf2_hmac('sha256',
                              password.encode(),
                              salt,
                              100000,
                              dklen=64)
    return key.hex()


def check_user(user_data: dict):
    con = create_db()

    user_name = user_data.get('account_name')
    password = user_data.get('password')
    query = 'SELECT password FROM users WHERE username = ?;'
    cur = con.cursor()
    cur.execute(query, (user_name,))
    x = cur.fetchone()
    if x:
        pass_hash = x[0]
        salt = b'\xf1\xccd7\xf1\x1dz\x8d\\\xa6/\x85\xf8\xb9-\x14\x1e\xed~\xa7\x92\n\x05\xab{$\xb5TD\xf2\xa2<'
        check = hashlib.pbkdf2_hmac('sha256',
                                    password.encode(),
                                    salt,
                                    100000,
                                    dklen=64)
        return check.hex() == pass_hash
    return


def get_data() -> dict:
    data_dict = {
        'username': input('input username: '),
        'password': input('input password: '),
        'first_name': input('input first_name: '),
        'last_name': input('input last_name: ')
    }
    return data_dict


def main():
    con = create_db()

    # ввод данных:
    # data = get_data()
    data = {
        'username': 'user1',
        'password': 'mypasword123',
        'first_name': 'First',
        'last_name': 'User'
    }
    data['password'] = get_hash_pass(data.get('password'))
    print(data)
    add_new_user(con, data)


if __name__ == '__main__':
    # con = create_db()
    # check_user(con, 1)
    print()
    # main()
