"""
Demo of threading module for chapter 8
"""

from dataclasses import dataclass
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
        # do some processing in the background...


def main():
    print('main thread is running')

    for facility in get_facilities_info():
        thread = FacilityRater(facility)
        thread.start()

    print('main thread is finished')


if __name__ == '__main__':
    main()
