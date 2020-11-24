import asyncio
import os
from asyncio import sleep
from asyncio.log import logger

import aiohttp
import aioredis
import ujson as json

API_URI_1 = os.getenv('API_URI_1', 'http://localhost:8001')
API_URI_2 = os.getenv('API_URI_2', 'http://localhost:8000')
REDIS_URI = os.getenv('REDIS_URI', 'redis://localhost')
NUMBERS_QUEUE = os.getenv('NUMBERS_QUEUE', 'published:numbers')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtaWNyb3NlcnZpY2VfaWQiOiIxMjM0NTY3ODkwIn0.l9u4wnxv7h0o8JwMgVCZ6p_bC19bBf5xQYIg3SsKCC0')
RATE_LIMIT = os.getenv('RATE_LIMIT', 0.5)


async def limit_wrap(session):
    odd_number = await fetch(session, API_URI_1)
    even_number = await fetch(session, API_URI_2)
    return json.loads(odd_number)['number'], json.loads(even_number)['number']


async def fetch(session, url):
    async with session.get(f'{url}/number/{ACCESS_TOKEN}') as response:
        return await response.text()


async def main():
    redis = await aioredis.create_redis_pool(REDIS_URI)

    async def publish(number):
        await redis.lpush(NUMBERS_QUEUE, number)

    async with aiohttp.ClientSession(headers={'Authorization': f'JWT {ACCESS_TOKEN}'}) as session:
        while True:
            try:
                numbers = await limit_wrap(session)
                product = numbers[0] * numbers[1]
                if product > 100000:
                    await publish(product)
            except Exception as e:
                logger.error(e)

            await sleep(RATE_LIMIT)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
