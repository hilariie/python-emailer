import pytest
import csv
import json
import socket
from ..email_processing import EmailProcessor, PyMailer

_original_connect = socket.socket.connect
false_directory = "false\\directory.fls"
recipient_test_data_list = {'names': ['hilary', 'henry'], 'emails': ['hilary@email.ng', 'henry@email.com']}
recipient_test_data = {'hilary': 'hil@email.ng', 'henry': 'henry@email.net'}
recipient_file_data = [['hilary', 'hilary@email.ng', 'cc@email.net'],
                       ['henry', 'henry@email.com']]
recipient_file_data_no_cc = [['hilary', 'hilary@email.ng'],
                             ['henry', 'henry@email.com']]
def patched_connect(*args, **kwargs):
    pass

@pytest.fixture
def empty_directory(tmpdir):
    fn = tmpdir.mkdir('empty_dir')
    return str(fn)


@pytest.fixture
def unempty_directory(tmpdir):
    fn = tmpdir.mkdir('unempty_dir')
    fn2 = fn.join('unempt_dir.txt')
    fn2.write("Hello")
    return str(fn)

@pytest.fixture(scope='session')
def csv_file_no_cc(tmpdir_factory):
    fn = tmpdir_factory.mktemp('csv_data2').join('recipients_no_cc.csv')
    headers = ['names', 'emails', 'cc']
    with open(fn, 'w', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(headers)

        # write multiple rows
        writer.writerows(recipient_file_data_no_cc)
    return str(fn)

@pytest.fixture(scope='session')
def csv_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp('csv_data').join('recipients.csv')
    headers = ['names', 'emails', 'cc']
    with open(fn, 'w', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(headers)

        # write multiple rows
        writer.writerows(recipient_file_data)
    with open(fn, 'r') as f:
        reader = csv.reader(f)
        reader = [lines for lines in reader]
    return str(fn)

@pytest.fixture
def json_file_list(tmpdir):
    fn = tmpdir.mkdir('json_data_list').join('recipients_list.json')
    with open(fn, 'w') as j_file:
        json.dump(recipient_test_data_list, j_file)
    return str(fn)


@pytest.fixture
def json_file(tmpdir):
    fn = tmpdir.mkdir('json_data').join('recipients.json')
    with open(fn, 'w') as j_file:
        json.dump(recipient_test_data, j_file)
    return str(fn)


@pytest.fixture
def html_file(tmpdir):
    fn = tmpdir.mkdir('html_data').join('email.html')
    fn.write("""<html>
    Hello,
    <p>
    How are you
    </p>
    </html>""")
    return str(fn)

@pytest.fixture
def txt_file(tmpdir):
    fn = tmpdir.mkdir('txt_data').join('email.txt')
    fn.write("""Hello,
    
    How are you""")
    return str(fn)

@pytest.fixture
def enable_network():
    socket.socket.connect = _original_connect
    yield
    socket.socket.connect = patched_connect

@pytest.fixture
def disable_network():
    socket.socket.connect = patched_connect
    yield
    socket.socket.connect = _original_connect

def correct_details():
    return ['correct.email@address.com', 'Password']
@pytest.fixture
def incorrect_details():
    return ['incorrect.email@address.com', 'incorrect_password']


def test_email_cleaner_empty_email():
    assert EmailProcessor().email_cleaner('') == ''

def test_email_cleaner_space():
    assert EmailProcessor().email_cleaner('hi h i hi') == 'hihihi'


def test_email_cleaner_dot():
    assert EmailProcessor().email_cleaner('d.o.t.com.') == 'd.o.t.com'


def test_email_cleaner_last_digit():
    assert EmailProcessor().email_cleaner('email@add.com3') == 'email@add.com'
    assert EmailProcessor().email_cleaner('email@add.1com') == 'email@add.com'
    assert EmailProcessor().email_cleaner('email@add.co2m') == 'email@add.com'

def test_email_checker_true():
    assert EmailProcessor().email_checker('email@address.ng') is True
    assert EmailProcessor().email_checker('Email@4me.net') is True


def test_email_checker_false():
    assert EmailProcessor().email_checker('email @email.com') is False
    assert EmailProcessor().email_checker('email@email.') is False
    assert EmailProcessor().email_checker('email@email.2com') is False


def test_email_content_reader(txt_file, html_file):

    assert EmailProcessor().email_content_file_reader(html_file) == """<html>
    Hello,
    <p>
    How are you
    </p>
    </html>"""
    assert EmailProcessor().email_content_file_reader(txt_file) == """Hello,
    
    How are you"""


def test_recipient_data(json_file, csv_file, csv_file_no_cc, json_file_list):
    ### Uncompleted Test function
    assert EmailProcessor().recipient_data(('email1', 'email2')) == ['email1', 'email2']
    assert 'email1' and 'email2' in EmailProcessor().recipient_data({'email1', 'email2'})
    assert EmailProcessor().recipient_data(['email1', 'email2']) == ['email1', 'email2']

    assert EmailProcessor().recipient_data({'name': 'email1', 'name2': 'email2'}) == [['name', 'name2'], ['email1', 'email2']]
    assert EmailProcessor().recipient_data(recipient_test_data_list) == [['hilary', 'henry'], ['hilary@email.ng', 'henry@email.com']]
    assert EmailProcessor().recipient_data('email1') == ['email1']
    with pytest.raises(FileNotFoundError, match=r".* doesn't exist"):
        EmailProcessor().recipient_data(false_directory)
    with pytest.raises(TypeError, match='email_recipient data should be in type: set, tuple, list, dict, str, or path'):
        EmailProcessor().recipient_data(None)
    # json fixture needs work
    assert EmailProcessor().recipient_data(json_file_list) == [['hilary', 'henry'], ['hilary@email.ng', 'henry@email.com']]
    assert EmailProcessor().recipient_data(json_file) == [['hilary', 'henry'], ['hil@email.ng', 'henry@email.net']]
    assert EmailProcessor().recipient_data(csv_file) == [['hilary', 'henry'], ['hilary@email.ng', 'henry@email.com'], ['cc@email.net']]
    assert EmailProcessor().recipient_data(csv_file_no_cc) == [['hilary', 'henry'], ['hilary@email.ng', 'henry@email.com']]
    # Uncompleted test


def test_recipient_dict_reader():
    assert EmailProcessor().recipient_dict_reader({'name': 'email1', 'name2': 'email2'}) == [['name', 'name2'], ['email1', 'email2']]


def test_recipient_dict_reader_list():
    assert EmailProcessor().recipient_dict_reader_list(recipient_test_data_list) == [['hilary', 'henry'], ['hilary@email.ng', 'henry@email.com']]


def test_recipient_csv_reader():
    with pytest.raises(FileNotFoundError, match=r".* not found in directory"):
        EmailProcessor().recipient_csv_reader(false_directory)


def test_file_attachments(unempty_directory, empty_directory):
    with pytest.raises(FileNotFoundError, match=r"Directory .* is empty"):
        EmailProcessor().file_attachments(empty_directory, 's')
    with pytest.raises(FileNotFoundError, match=r".* doesn't exist"):
        EmailProcessor().file_attachments(false_directory, 's')
    with pytest.raises(ValueError, match='file names not equal to number of files in directory'):
        EmailProcessor().file_attachments(unempty_directory, 's', ['j', 'sd'])


def test_smtp_checker():
    assert EmailProcessor().smtp_checker('ag@gmail.com') == 'smtp.gmail.com'
    assert EmailProcessor().smtp_checker('ag@hotmail.com') and \
           EmailProcessor().smtp_checker('email@outlook.net') == 'smtp-mail.outlook.com'
    assert EmailProcessor().smtp_checker('email@yahoo.com') == 'smtp.mail.yahoo.com'

def test_email_receiver_processing():
    ### Not sure about this test
    assert PyMailer(recipient_test_data, [''], '', '').email_receiver_processing() == ({'hilary': 'hil@email.ng', 'henry': 'henry@email.net'}, '')
    assert PyMailer(recipient_test_data_list, [''], '', '').email_receiver_processing() == ({'hilary': 'hilary@email.ng', 'henry': 'henry@email.com'}, '')




def test_email_body_processing():
    assert PyMailer(recipient_test_data, [''], '', '').email_body_processing('email test') == ('email test', '.txt')
    assert PyMailer(recipient_test_data, [''], '', '').email_body_processing("<html> email test </html>") == ("<html> email test </html>", '.html')
    assert PyMailer(recipient_test_data, [''], '', "html email test").email_body_processing("html email test") == ("html email test", '.txt')
    # TEst for directory

