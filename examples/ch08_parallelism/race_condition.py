"""
Demo of a race condition between processes
"""

from dataclasses import dataclass
from multiprocessing import Lock
from random import random
from threading import Thread
from time import sleep

from typing_extensions import ClassVar


@dataclass
class Counter:
    value: int = 0


@dataclass
class Facility:
    name: str
    city: str
    state: str

    def __str__(self):
        return f'{self.name} {self.city} {self.state}'


def get_facilities_info():
    for i in range(0, 1000):
        yield Facility(f'Facility {i}', 'Sacremento', 'CA'),


class FacilityRater(Thread):
    lock: ClassVar[Lock] = Lock()

    def __init__(self, facility, counter):
        super().__init__()
        self.facility = facility
        self.shared_counter = counter

    def run(self):
        with FacilityRater.lock:
            self.shared_counter.value += 1
            self.rating = self.rate_facility()

    def rate_facility(self):
        return 50 + random() * 50


def main():
    print('main thread is running')

    counter = Counter(0)

    rating_threads = []
    for facility in get_facilities_info():
        thread = FacilityRater(facility, counter)
        thread.start()
        rating_threads.append(thread)

    print(f'started {len(rating_threads)} facility rating processes')

    for thread in rating_threads:
        thread.join()

    print(f'{counter.value} facility ratings completed')
    best = max(rating_threads, key=lambda thread: thread.rating)
    print(f'highest rating out of {len(rating_threads)} facilities '
          f'is {best.rating:.1f}% for {best.facility}')


if __name__ == '__main__':
    main()
