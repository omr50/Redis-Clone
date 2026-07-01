import asyncio
from RESP import parse, parseArray, encode
from commands import executeCommand

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    # print("connected by", addr)
    buffer = ""
    command = ""

    while True:
        chunk = await reader.read(4096)
        if not chunk:
            break
        try:
            buffer += chunk.decode()
            parsedArray, end = parseArray(buffer)
            if end == len(buffer):
                command = parsedArray 
                buffer = ""
            elif end < len(buffer):
                command = parsedArray
                buffer = buffer[end:]
            res = executeCommand(command)
            encodedRes = encode(res)
            writer.write(encodedRes.encode())
            await writer.drain()
        except Exception as e:
            print(type(e), e)
            print(repr(buffer))


    writer.close()
    await writer.wait_closed()
