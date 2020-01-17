"""
Example of initializing a dictionary from a CSV file
"""

payroll = {}  # initialize with an empty dictionary

with open('payroll_records.csv') as csv_file:
    record_count = 0
    for line in csv_file:
        if record_count > 0:       # skip header line
            line = line.strip()    # remove newline
            row = line.split(',')  # row is a list of string
            emp_id = row[0]
            hours_worked = row[1]
            payroll[emp_id] = hours_worked
        record_count += 1

print(f'read {record_count} records')

hours = payroll.get('4321')  # look up by emp ID
print(f'Employee 4231 worked {hours} hours')
