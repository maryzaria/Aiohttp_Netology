import aiohttp
from asyncio import run


async def main():

    async with aiohttp.ClientSession() as session:
        # response = await session.post('http://127.0.0.1:8080/users/', json={'username': 'user3', 'password': '1234'})
        # print(await response.json())
        response = await session.get("http://127.0.0.1:8080/users/3")
        print(await response.json())
        response = await session.delete("http://127.0.0.1:8080/users/3")
        print(await response.json())

        response = await session.get("http://127.0.0.1:8080/users/3")
        print(await response.json())


run(main())
