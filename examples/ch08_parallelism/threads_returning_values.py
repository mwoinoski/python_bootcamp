"""
Demo of retrieving values from threads after they complete their tasks.
"""

from dataclasses import dataclass
from random import random
from threading import Thread
from typing import Optional, List


@dataclass
class Facility:
    name: Optional[str]
    city: Optional[str]
    state: Optional[str]

    def __str__(self):
        return f'{self.name} {self.city} {self.state}'


def get_facilities_info():
    return [
        Facility('Getwell Hospital', 'Sacremento', 'CA'),
        Facility('Qwik-E-Health Emergent Care', 'Denver', 'CO'),
        Facility('Bonecrakin Chiropractic', 'New York', 'NY'),
    ]


class FacilityRater(Thread):
    def __init__(self, facility):
        super().__init__()
        self.facility = facility

    def run(self):
        print(f'rating facility {self.facility} in new thread')
        self.rating = self.rate_facility()

    def rate_facility(self):
        return 50 + random() * 50


def main():
    rating_threads = []

    for facility in get_facilities_info():
        thread = FacilityRater(facility)
        thread.start()
        rating_threads.append(thread)

    for thread in rating_threads:
        thread.join()

    print('\nratings for facilities:')
    for thread in rating_threads:
        print(f'\t{thread.facility}: {thread.rating:.1f}%')

    best = max(rating_threads, key=lambda thread: thread.rating)

    print(f'\nhighest rating is {best.rating:.1f}% for {best.facility}')


if __name__ == '__main__':
    main()
