import pytest
from RESP import parseString, parseError

@pytest.mark.parametrize("raw, expected", [
    ("+OK\r\n", "OK"),
    ("+PONG\r\n", "PONG"),
    ("+hello world\r\n", "hello world"),
    ("+\r\n", ""),
])

def test_parse_string_valid_simple_strings(raw, expected):
    assert parseString(raw) == expected

@pytest.mark.parametrize("raw, expected", [
    ("-ERROR MESSAGE\r\n", "ERROR MESSAGE"),
    ("-WRONG\r\n", "WRONG"),
    ("-\r\n", ""),
])
def test_parseError(raw, expected):
    assert parseError(raw) == expected
