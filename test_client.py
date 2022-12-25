import unittest

from client.utils import read_msg, auth_user_msg, quit_user_msg


class TestPayment(unittest.TestCase):

    def test_add_balance(self):
        input_data = b'{"response": 200, "alert": "OK"}'
        output_data = {'response': 200, 'alert': 'OK'}
        res = read_msg(input_data)
        self.assertEqual(res, output_data)

    def test_auth_user_msg(self):
        user = 'user_test'
        password = '12345'
        res = auth_user_msg(user, password)
        res['time'] = 1671878468.9642105
        output_data = {
            'action': 'authenticate',
            'time': 1671878468.9642105,
            'user': {'account_name': 'user_test', 'password': '12345'}
        }
        self.assertEqual(res, output_data)

    def test_quit_user_msg(self):
        user = 'user_test'
        res = quit_user_msg(user)
        res['time'] = 1671878468.9642105
        output_data = {
            'action': 'quit',
            'time': 1671878468.9642105,
            'user': {'account_name': 'user_test'}
        }
        self.assertEqual(res, output_data)



if __name__ == '__main__':
    unittest.main()