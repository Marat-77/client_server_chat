import pytest

from server.utils import check_auth
from server.models import get_hash_pass

user_dict1 = {"account_name": "user1",
             "password": "mypasword123"}
user_dict2 = {"account_name": "user1",
             "password": "wrongpasword"}
users1 = {'user2'}
users = {'user1', 'user2'}
res1 = ({'response': 200, 'alert': 'OK'}, 'user1')
res2 = (
    {
    'error': 'This could be "wrong password" or "no account with that name"',
    'response': 402
    },
    None
)
res3 = (
    {
    'error': 'Someone is already connected with the given user name',
    'response': 409
    },
    None
)
results = [(user_dict1, users1, res1),
           (user_dict2, users1, res2),
           (user_dict1, users, res3)]


@pytest.mark.parametrize('user_data, auth_users, expected_result', results)
def test_check_auth(user_data, auth_users, expected_result):
    assert check_auth(user_data, auth_users) == expected_result


results = [
    ('123', '69273e4276ddfbf79e3fbad36db0f01dea37b995e78e97fd8ebb0ec2c77630e4b268bb5fea97e7544854c44df2db804267f2f7fc73e6bcc081138f7c606f2653'),
    ('abc', '1c568fffecc471ec8a8d4954cdd9237a3fef7aff71037554427722d933722263d5c96b901f1b56b55b25afaf8429b174498bf3dd6774105a02389141de543786'),
    ('абв', '6ec557dda863d033784f7f3f161918273d260e62bb0b01dbd13d0aded4c72ffd50f99ea759e81bdc86029cb58799acad55e4edf7b524f00e1f053c0deb67982f'),
    (123, None),
    ('', '945f43bf0e2b9bae36d162ff6e97317375e876a2876950c6dab859eb6c99844a9cbcc8485a61e8cf372d18f857597e1eaefd81b490ff947c4bb21ab59534af35'),
    (None, None)
]


@pytest.mark.parametrize('password, expected_result', results)
def test_get_hash_pass(password, expected_result):
    assert get_hash_pass(password) == expected_result

