"""
Find facilities that have duplicate CMS Certification Numbers (CCN)
"""

import sys


# TODO: note the definition of the function main() (no code changes required)
def main(filepath) -> int:

    # TODO: initialize a `facilities` variable with an empty dictionary
    facilities = {}

    # TODO: open the file facility_perf_scores.csv
    with open(filepath) as csv_file:
        # TODO: initialize a record counter to 0
        record_count = 0
        # TODO: loop over each line of the  CSV file
        for line in csv_file:
            # TODO: skip the header line
            if record_count > 0:
                # TODO: remove the newline character from the input line
                line = line.strip()
                # TODO: split the line at the comma separators
                row = line.split(',')
                # TODO: get the facility name and certification number from the row
                fac_name = row[0]
                fac_cert_num = row[1]
                # TODO: add the certification number to the `facilitites` dictionary
                #       using the facility name as the key
                facilities[fac_name] = fac_cert_num
            # TODO: increment the record counter
            record_count += 1

    # TODO: print the record count
    print(f'Read {record_count} facilities')

    # facilities = {'General Hospital': '123', 'Acme Clinic': '532', 'Best ER': '123'}

    # TODO: initialize a `flipped` variable with an empty dictionary
    flipped = {}

    # TODO: loop over all the facility names in `facilities`
    for fac_name in facilities:
        # TODO: get the facility's cert number
        fac_cert_num = facilities.get(fac_name)
        # TODO: get the list of facility names with that cert number
        facility_list = flipped.get(fac_cert_num)
        # TODO: if the list of names is None, add an item to `flipped` with the
        # cert number as the key. The value of the item is an empty list
        if not facility_list:
            flipped[fac_cert_num] = []
        # TODO: append the facility name to the list of names for this cert num
        # HINT: see slide 70
        flipped[fac_cert_num].append(fac_name)

    dupe_count = 0

    # TODO: loop through all the items in the `flipped` dictionary
    for fac_cert_num in flipped:
        # TODO: get the list of facilities with this cert number
        facilities_with_same_ccn = flipped.get(fac_cert_num)
        # TODO: if the length of the list is greater than 1, print out the list.
        # Also, keep a count of the number of duplicate cert numbers
        if len(facilities_with_same_ccn) > 1:
            dupe_count += 1
            print(f'facilities with ID {fac_cert_num}: {facilities_with_same_ccn}')

    # TODO: print the number of duplicate cert numbers. Be sure the message is
    # grammatically correct ('Found 1 duplicate CCN', 'Found 2 duplicate CCNs')
    if dupe_count != 1:
        print(f'Found {dupe_count} duplicate CCNs')
    else:
        print(f'Found 1 duplicate CCN')
    # print(f'Found {dupe_count} duplicate CCN{"s" if dupe_count != 1 else ""}')

    # TODO: return the number of duplicate cert numbers
    return dupe_count


if __name__ == '__main__':
    main(sys.argv[1])
