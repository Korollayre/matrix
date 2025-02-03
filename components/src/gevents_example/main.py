from datetime import datetime

import gevent
from gevent import monkey

monkey.patch_all()

# pylint: disable-next=wrong-import-position
import requests    # noqa

URL = 'https://www.python.org/'


def send(number: int):
    print(f'Starting {number}')
    res = requests.get(URL, timeout=5).text
    assert res
    print(f'End {number}')


def decorator(func):

    def wrapper():
        start_moment = datetime.now()
        func()
        end_moment = datetime.now()
        delta = (end_moment - start_moment).total_seconds()
        print(f'Time for [{func.__name__}] - [{delta}]')

    return wrapper


@decorator
def send_with_gevents():
    jobs = [gevent.spawn(send, number) for number in range(10)]
    gevent.joinall(jobs)


@decorator
def send_without_gevents():
    for number in range(10):
        send(number)


if __name__ == '__main__':
    send_without_gevents()
    send_with_gevents()
