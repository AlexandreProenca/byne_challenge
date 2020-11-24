from typing import Dict
import time
from flask import Flask
from flask import abort
import random
import os
from jose import JWTError, jwt

app = Flask(__name__)

KIND_NUMBER = os.getenv('KIND_NUMBER')
SECRET_KEY = os.getenv('SECRET_KEY', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')


def _generate_number() -> int:
    return random.choices(
            [n for n in range(1001) if n % 2 != 0] if KIND_NUMBER == 'odd' else [n for n in range(1001) if n % 2 == 0]
        )[0]


@app.route('/number/<token>', methods=['GET'])
def get_number(token) -> Dict[str, int]:
    """ This method gives a random integer number, odd or even, the kind of number delivered dependes the KIND_NUMBER
    enviroument variable, it uses a signed token to keep this endpoint secure.
    It returns a json response with key 'number' and a integer on value like this {"number": 324}.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        microservice_id: str = payload.get("microservice_id")
        if microservice_id is None:
            abort(404)  # Not response the real HTTP code to avoid buteforce attacks

        number = _generate_number()

        # Log tracking wich microservices get wich number, logs always helps to find and solve bugs :)
        app.logger.info(f'\t micoservice::{microservice_id}::GET::{number}::timestamp::{int(time.time())}')

        return {"number": number}

    except JWTError:
        raise abort(404)  # Not response the real HTTP code to avoid buteforce attacks


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
