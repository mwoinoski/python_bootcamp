"""
Demo of the ThreadPoolExecutor for chapter 8
"""

from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import as_completed
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
        Facility('A+ Emergent Care', 'Cincinnati', 'OH'),
        Facility('Lone Star Clinic', 'Austin', 'TX'),
    ]


def rate_facility(facility):
    try:
        print(f'rating facility {facility} in new thread from pool')
        rating = 50 + random() * 50
        if rating < 55:
            raise RuntimeError(f'lower rating for {facility}', rating)
        return facility, rating
    except Exception as ex:
        raise RuntimeError(facility) from ex


def main():
    rating_futures = []

    for facility in get_facilities_info():
        with ProcessPoolExecutor(max_workers=20) as executor:
            future = executor.submit(rate_facility, facility)
            rating_futures.append(future)

    successfully_processed = []
    failed_tasks = []

    for future in as_completed(rating_futures):
        err = future.exception()
        if not err:
            successfully_processed.append(future.result())
        else:
            failed_tasks.append(err.args[0])  # facility

    print('\nratings for facilities:')

    for facility, rating in sorted(successfully_processed, reverse=True,
                                   key=lambda x: x[1]):
        print(f'\t{facility}: {rating:.1f}%')

    if failed_tasks:
        print(f'\nrating process failed for {len(failed_tasks)} facilities:')
        for facility in failed_tasks:
            print(f'\t{facility}')


if __name__ == '__main__':
    main()
