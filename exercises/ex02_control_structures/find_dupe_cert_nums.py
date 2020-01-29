"""
Find facilities that have duplicate CMS Certification Numbers (CCN)
"""
import sys


# TODO: note the definition of the function main() (no code changes required)
def main(filepath) -> int:

    # Code initialize a dictionary from a CSV file:
    # payroll = {}  # initialize with an empty dictionary
    # with open('payroll_records.csv') as csv_file:
    #     record_count = 0
    #     for line in csv_file:
    #         if record_count > 0:       # skip header line
    #             line = line.strip()    # remove newline
    #             row = line.split(',')  # row is a list of string
    #             emp_id = row[0]
    #             hours_worked = row[1]
    #             payroll[emp_id] = hours_worked
    #         record_count += 1

    # ------------------------------------------------------------------------------
    # FIRST TASK: read a CSV file into a dictionary. The result will look like this:
    # facilities = {'General Hospital': '123', 'Acme Clinic': '532', 'Best ER': '123'}
    # ------------------------------------------------------------------------------

    # TODO: initialize a `facilities` variable with an empty dictionary
    facilities = ....

    # TODO: open the file facility_perf_scores.csv
    with ....
        # TODO: initialize a record counter to 0

        # TODO: loop over each line of the  CSV file

            # TODO: skip the header line

                # TODO: remove the newline character from the input line

                # TODO: split the line at the comma separators

                # TODO: get the facility name and certification number from the row


                # TODO: add the certification number to the `facilitites` dictionary
                #       using the facility name as the key

            # TODO: increment the record counter


    # TODO: print the record count

    # facilities = {'General Hospital': '123', 'Acme Clinic': '532', 'Best ER': '123'}

    # ------------------------------------------------------------------------------
    # NEXT TASK: create a `flipped` dictionary where each key is a certification
    # number and each value is a list of all facilities with that cert number.
    # `flipped` will look like this:
    # flipped = {'123': ['General Hospital', 'Best ER'], '532': ['Acme Clinic']}
    # ------------------------------------------------------------------------------

    # HINT: code to loop over dictionary items:
    # for key in the_dict:
    #     value = the_dict.get(key)
    #     print(f'option {key} has value {value}')

    # TODO: initialize a `flipped` variable with an empty dictionary
    flipped = ....

    # TODO: loop over all the facility names in `facilities`

        # TODO: get the facility's cert number

        # TODO: get the list of facility names with that cert number

        # TODO: if the list of names is None, add an item to `flipped` with the
        # cert number as the key. The value of the item is an empty list


        # TODO: append the facility name to the list of names for this cert num
        # HINT: see slide 70


    # ------------------------------------------------------------------------------
    # FINAL TASK: loop through the `flipped` dictionary and print out all the
    # facilities that have duplicate cert nums
    # ------------------------------------------------------------------------------

    dupe_count = ....

    # TODO: loop through all the items in the `flipped` dictionary

        # TODO: get the list of facilities with this cert number

        # TODO: if the length of the list is greater than 1, print out the list.
        # Also, keep a count of the number of duplicate cert numbers



    # TODO: print the number of duplicate cert numbers. Be sure the message is
    # grammatically correct ('Found 1 duplicate CCN', 'Found 2 duplicate CCNs')


    # TODO: return the number of duplicate cert numbers
    return ....


if __name__ == '__main__':
    main(sys.argv[1])
