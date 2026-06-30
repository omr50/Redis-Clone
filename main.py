import asyncio
from TCP_Server import handle_client

async def main():
    server = await asyncio.start_server(
        handle_client,
        "127.0.0.1",
        6379
    )
    async with server:
        await server.serve_forever()

asyncio.run(main())