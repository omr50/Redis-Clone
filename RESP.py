# Common values
CRLF = '\r\n'

def parseString(input):
    if input[0] != '+' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: String")
    return input[1:-2]


def parseError(input):
    if input[0] != '-' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: Error")
    return input[1:-2]

