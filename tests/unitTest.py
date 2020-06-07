import sys
sys.path.insert(1, "../")

import io
from unittest.mock import Mock
import main


def test_print_name():
    name = 'test'
    data = {'name': name}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert main.hello_http(req) == 'Hello {}!'.format(name)

def test_file_name():
    data = {"name": "image"}
    data['file'] = (io.BytesIO(b"abcdef"), './img/logo_full.png')
    req = Mock(get_json=Mock(return_value=data), args=data)

    assert main.iconGenerator(req) == 'attached file {}!'.format("logo_full.png")

def test_print_hello_world():
    data = {}
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    assert main.hello_http(req) == 'Hello World!'