from src.utility import *

ASSETS_FOLDER = "assets"
USER_DATA_CSV = "user_data.csv"


def test_create_csv():
    create_csv()
    assert os.path.exists(os.path.join(ASSETS_FOLDER, USER_DATA_CSV))


def test_save_and_check_csv():
    user_data = {'username': 'test', 'password_hash': 'hashed_password'}
    save_to_csv(user_data)

    assert is_present_in_csv('test')
    assert not is_present_in_csv('nonexistent_user')


def test_get_password():
    user_data = {'username': 'test2', 'password_hash': 'hashed_password2'}
    save_to_csv(user_data)

    assert get_password('test2') == 'hashed_password2'
    assert get_password('nonexistent_user') is None


def test_hash_and_check_password():
    hash_val = hash_password('password')
    assert check_password('password', hash_val)
    assert not check_password('wrong_password', hash_val)
