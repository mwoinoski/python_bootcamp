"""
Driver for Health Care Facility application
"""

import sys
import csv

from facilities.dialysis_facility import DialysisFacility
from facilities.hospital import Hospital


def main(path):
    """ Populate objects for the health care facilities """
    print(f'reading file {path}')
    facilities = read_facilities_data_file(path)

    print(f'\nProcessing {len(facilities)} facilities\n')
    for facility in facilities:
        score = facility.calculate_quality_score()
        print(f'{facility}: quality score {score}')


def read_facilities_data_file(path):
    with open(path, newline='') as csvfile:
        facilities = []
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if csvreader.line_num > 1:
                addr = f'{row[2]} {row[3]} {row[4]} {row[5]}'
                facility_type = row[6].upper()
                if facility_type == 'H':
                    facility = Hospital(int(row[0]), row[1], addr, int(row[7]))
                elif facility_type == 'D':
                    facility = DialysisFacility(int(row[0]), row[1], addr,
                                                int(row[8]))
                else:
                    raise ValueError(f'unknown facility type "{facility_type}"')

                facilities.append(facility)
    return facilities


if __name__ == '__main__':
    print(f'Starting Health Care Facility application')
    main(sys.argv[1])
