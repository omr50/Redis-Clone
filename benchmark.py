import asyncio
import time

HOST = "127.0.0.1"
PORT = 6379

CLIENTS = 50
REQUESTS_PER_CLIENT = 1000

SET_CMD = b"*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n"
GET_CMD = b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n"

async def client_worker():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    count = 0

    for _ in range(REQUESTS_PER_CLIENT):
        writer.write(SET_CMD)
        await writer.drain()
        await reader.readuntil(b"\r\n")
        await reader.readuntil(b"\r\n")

        writer.write(GET_CMD)
        await writer.drain()
        await reader.readuntil(b"\r\n")
        await reader.readuntil(b"\r\n")

        count += 2

    writer.close()
    await writer.wait_closed()
    return count

async def main():
    start = time.perf_counter()

    results = await asyncio.gather(
        *(client_worker() for _ in range(CLIENTS))
    )

    end = time.perf_counter()
    total = sum(results)

    print(f"{CLIENTS} clients")
    print(f"{total} total requests")
    print(f"{total / (end - start):.0f} requests/sec")

asyncio.run(main())