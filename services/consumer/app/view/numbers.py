import logging
import os
import time
from typing import Dict

import aioredis
from fastapi import APIRouter, HTTPException, status
from fastapi.logger import logger
from jose import JWTError, jwt

router = APIRouter()

NUMBERS_QUEUE = os.getenv('NUMBERS_QUEUE', 'published:numbers')
REDIS_URI = os.getenv('REDIS_URI', 'redis://byne_redis_1')
SECRET_KEY = os.getenv('SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')


@router.get("/{token}")
async def get_numbers(token) -> Dict[str, int]:
    """This method return latest 100 numbers retained on redis database,
    it use a signed token to keep this endpont safe.
    """
    logging.basicConfig(level=logging.INFO)
    redis = await aioredis.create_redis_pool(REDIS_URI)

    security_exception = HTTPException(  # Not response the real HTTP code to avoid buteforce attacks
        status_code=status.HTTP_404_NOT_FOUND,
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise security_exception

        numbers = await redis.lrange(NUMBERS_QUEUE, 0, 99)
        logger.info(f'Client::{token}::GET::{numbers}::timestamp::{int(time.time())}')
        redis.close()
        await redis.wait_closed()
        return {"numbers": numbers}

    except JWTError:
        raise security_exception
