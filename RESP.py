# Common values
CRLF = '\r\n'

# ------------------- ENCODER --------------------------
def parse(input):
    identifier = input[0]
    if identifier == '+':
        return parseString(input)
    if identifier == '-':
        return parseError(input)
    if identifier == '$':
        return parseBulkString(input)
    if identifier == '*':
        return parseArray(input)
    if identifier == ':':
        return parseInteger(input)
    return input

def parseString(input):
    if input[0] != '+' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: String")
    return input[1:-2]


def parseError(input):
    if input[0] != '-' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: Error")
    return input[1:-2]

def parseInteger(input):
    if input[0] != ':' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: Integer")
    return int(input[1:-2])

def deriveLength(input, start):
    lengthNum = ""
    endOfLenIndex = start
    for i in range(start, len(input)):
        if input[i].isdigit():
            lengthNum += input[i]
        else:
            endOfLenIndex = i
            break

    return (int(lengthNum), endOfLenIndex)

def parseBulkString(input):
    if input[0] != '$' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: Bulk String")

    # null bulk string
    if input == '$-1\r\n':
        return None
    if input == '$0\r\n\r\n':
        return ""
    lengthNum, endOfLenIndex = deriveLength(input, 1)

    if len(CRLF) + endOfLenIndex + lengthNum + len(CRLF) != len(input):
        raise ValueError("Incorrect length for type: Bulk String")
    if input[endOfLenIndex: endOfLenIndex+2] != CRLF:
        raise ValueError("Missing ending CRLF for type: Bulk String")

    bulkString = input[endOfLenIndex+2: -2]
    return bulkString

def findEnd(input):
    if input.find(CRLF) == -1:
        raise ValueError("Malformed input")
    if input[0] in "+-:" or input == '$-1\r\n':
        return input.find(CRLF) + 1
    if input[0] == '$':
        if input.startswith("$0\r\n\r\n"):
            return 5
        firstCRLFLoc = input.find(CRLF) + 1
        if input[firstCRLFLoc + 2: ].find(CRLF) == -1:
            raise ValueError("Malformed input")
        return firstCRLFLoc + 2 + input[firstCRLFLoc + 2: ].find(CRLF) + 1

def parseArray(input):
    if input[0] != '*' and input[-2:] != CRLF:
        raise ValueError("Incorrect format for type: Array")
    numElements, endOfLenIndex = deriveLength(input, 1)

    # parse out number of elements using split with \r\n as the delimiter
    cleanedInput = input[endOfLenIndex:]
    outputArr = []
    prevIndex = 0
    index = 0 
    commands = ('+', '*', '-', ':', '$')
    while index < len(cleanedInput) and numElements > 0: 
        currInput = cleanedInput[index]
        if cleanedInput[index: index+2] == CRLF:
            index = index + 2
            continue
        if currInput in commands:
            element = ""
            if currInput == '*':
                element, nextIndex = parseArray(cleanedInput[index:])
                index += nextIndex
            else:
                endOfElem = findEnd(cleanedInput[index:])
                element = parse(cleanedInput[index:index + endOfElem + 1])
                index += endOfElem + 1
            numElements -= 1
            outputArr.append(element)
        if index == prevIndex:
            raise ValueError("Malformed Input")
    return outputArr, endOfLenIndex + index

# print(parseArray("*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"))
# print(parseArray("*2\r\n$12\r\nabcde673jelz\r\n:3\r\n"))
# print(parseArray("*3\r\n:1\r\n*2\r\n+foo\r\n+bar\r\n*1\r\n*2\r\n:10\r\n:20\r\n"))


# ------------------- ENCODER --------------------------

# def encodeString(input):
#     return "+" + input + CRLF

# def encodeError(input):
#     return "-" + input + CRLF 
def encode(input):
    if isinstance(input, str):
        return encodeBulkString(input)
    elif isinstance(input, list):
        return encodeArray(input)
    elif isinstance(input, int):
        return encodeInteger(input)
    elif input is None:
        return encodeBulkString(None)
    else:
        raise ValueError("Malformed array")

def encodeInteger(input):
    return ":" + str(input) + CRLF

def encodeBulkString(input):
    if input == None:
        return "$-1\r\n"
    return "$" + str(len(input)) + CRLF + input + CRLF 

def encodeArray(input):
    output = "*" + str(len(input)) + CRLF
    for elem in input:
        output += encode(elem)
    return output

