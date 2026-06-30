import pytest
from RESP import parseString, parseError, parseInteger, parseArray, parseBulkString, findEnd
from RESP import encodeInteger, encodeArray, encodeBulkString

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

@pytest.mark.parametrize("raw, expected", [
    (":123\r\n", 123),
    (":-123\r\n", -123), 
])
def test_parseInteger(raw, expected):
    assert parseInteger(raw) == expected

@pytest.mark.parametrize("raw", [":-123a\r\n", ":zk\r\n", ":124.58\r\n"])
def test_parseIntegerError(raw):
    with pytest.raises(ValueError):
        parseInteger(raw)

@pytest.mark.parametrize("raw, expected", [
    ("$12\r\nabcde673jelz\r\n", "abcde673jelz"),
    ("$3\r\nabc\r\n", "abc"),
    ("$0\r\n\r\n", ""),
])
def test_parseBulkString(raw, expected):
    assert parseBulkString(raw) == expected
    
@pytest.mark.parametrize("raw", ["$2\r\na\r\n", "$3\r\n\r", "4\r\nabcdef\r\n"])
def test_parseBulkStringError(raw):
    with pytest.raises(ValueError):
        parseBulkString(raw)


@pytest.mark.parametrize("raw, expected", [
    ("*2\r\n$12\r\nabcde673jelz\r\n:3\r\n", ["abcde673jelz", 3]),
    ("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n", ["hello", "world"]),
    ("*3\r\n:1\r\n*2\r\n+foo\r\n+bar\r\n*1\r\n*2\r\n:10\r\n:20\r\n", [1,["foo", "bar"],[[10, 20]]]),
    ("*0\r\n", []),
    ("*3\r\n:1\r\n:2\r\n:3\r\n", [1, 2, 3]),
    ("*2\r\n$0\r\n\r\n+OK\r\n", ["", "OK"]),
    ("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n", ["hello", "world"]),
    ("*3\r\n:1\r\n*2\r\n+foo\r\n+bar\r\n*1\r\n*2\r\n:10\r\n:20\r\n", [1, ["foo", "bar"], [[10, 20]]]),
    ("*4\r\n+OK\r\n-ERR bad thing\r\n:123\r\n$5\r\nhello\r\n", ["OK", "ERR bad thing", 123, "hello"]),
    ("*2\r\n*0\r\n*0\r\n", [[], []]),
    ("*3\r\n*1\r\n+one\r\n*2\r\n:2\r\n:3\r\n*3\r\n+four\r\n+five\r\n+six\r\n", [["one"], [2, 3], ["four", "five", "six"]]),
    ("*1\r\n*1\r\n*1\r\n*1\r\n+deep\r\n", [[[[ "deep" ]]]]),
    ("*2\r\n$11\r\nhello world\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n", ["hello world", ["foo", "bar"]]),
    ("*5\r\n:0\r\n:-1\r\n:999999\r\n$0\r\n\r\n+END\r\n", [0, -1, 999999, "", "END"]),
    ("*3\r\n*2\r\n$3\r\nfoo\r\n:10\r\n*2\r\n$3\r\nbar\r\n:20\r\n*2\r\n$3\r\nbaz\r\n:30\r\n", [["foo", 10], ["bar", 20], ["baz", 30]]),
    ("*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n*2\r\n+yes\r\n+no\r\n*1\r\n$4\r\ntest\r\n",[[1, 2, 3], [["yes", "no"], ["test"]]]),
    ])

def test_parseArray(raw, expected):
    assert parseArray(raw)[0] == expected

@pytest.mark.parametrize("raw, expected", [
    ("$12\r\nabcde673jelz\r\n", 18),
    ("$3\r\nabc\r\n", 8),
    (":3\r\n", 3),
    (":34\r\n", 4), 
])
def test_findEnd(raw, expected):
    assert findEnd(raw) == expected


@pytest.mark.parametrize("value, expected", [
    (123, ":123\r\n"),
    (-123, ":-123\r\n"),
])
def test_encodeInteger(value, expected):
    assert encodeInteger(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("abcde673jelz", "$12\r\nabcde673jelz\r\n"),
    ("abc", "$3\r\nabc\r\n"),
    ("", "$0\r\n\r\n"),
])
def test_encodeBulkString(value, expected):
    assert encodeBulkString(value) == expected


@pytest.mark.parametrize("value, expected", [
    (["abcde673jelz", 3], "*2\r\n$12\r\nabcde673jelz\r\n:3\r\n"),
    (["hello", "world"], "*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"),
    ([1, ["foo", "bar"], [[10, 20]]], "*3\r\n:1\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n*1\r\n*2\r\n:10\r\n:20\r\n"),
    ([], "*0\r\n"),
    ([1, 2, 3], "*3\r\n:1\r\n:2\r\n:3\r\n"),
    (["", "OK"], "*2\r\n$0\r\n\r\n$2\r\nOK\r\n"),
    (["OK", "ERR bad thing", 123, "hello"], "*4\r\n$2\r\nOK\r\n$13\r\nERR bad thing\r\n:123\r\n$5\r\nhello\r\n"),
    ([[], []], "*2\r\n*0\r\n*0\r\n"),
    ([["one"], [2, 3], ["four", "five", "six"]], "*3\r\n*1\r\n$3\r\none\r\n*2\r\n:2\r\n:3\r\n*3\r\n$4\r\nfour\r\n$4\r\nfive\r\n$3\r\nsix\r\n"),
    ([[[["deep"]]]], "*1\r\n*1\r\n*1\r\n*1\r\n$4\r\ndeep\r\n"),
    (["hello world", ["foo", "bar"]], "*2\r\n$11\r\nhello world\r\n*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n"),
    ([0, -1, 999999, "", "END"], "*5\r\n:0\r\n:-1\r\n:999999\r\n$0\r\n\r\n$3\r\nEND\r\n"),
    ([["foo", 10], ["bar", 20], ["baz", 30]], "*3\r\n*2\r\n$3\r\nfoo\r\n:10\r\n*2\r\n$3\r\nbar\r\n:20\r\n*2\r\n$3\r\nbaz\r\n:30\r\n"),
    ([[1, 2, 3], [["yes", "no"], ["test"]]], "*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n*2\r\n$3\r\nyes\r\n$2\r\nno\r\n*1\r\n$4\r\ntest\r\n"),
])
def test_encodeArray(value, expected):
    assert encodeArray(value) == expected

'''
handling array

- it can contain any type, thinking of how to parse, or chop since simple crlf delimiter wont work
- was thinking i can only use crlf as a delimiter conditionally
    - We can use the crlf if isn't in front of a new element (identified by *, +, $, -)
- the only problem is that what if we have a nested bulk array?
- thinking of having a parsing loop which determines if the types are any other type then we
  can separate, otherwise if bulk array recursively call this bulk array function on it
    - the issue when calling the inner function then how does that one know to end?
    - i think the array parser can basically just stop at it's total elements?
    - so like *3 would do the first 3 and return

'''