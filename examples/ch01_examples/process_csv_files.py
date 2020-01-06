"""
Functions to process CSV files.
"""
import csv
import sys


def read_csv_file_hard_to_test(filepath):
    with open(filepath, newline='') as input_stream:
        lines = []
        spamreader = csv.reader(input_stream, quoting=csv.QUOTE_NONNUMERIC)
        for row_num, row in enumerate(spamreader):  # row is List of string
            if row_num == 0:
                header = row
            else:
                lines.append(row)
    return header, lines


def read_csv_file(filepath):
    # TODO: validate parameter values, raise exception if bad
    with open(filepath, newline='') as input_stream:
        return read_csv_stream(input_stream)


def read_csv_stream(input_stream):
    # TODO: validate parameter values, raise exception if bad
    records = []
    spamreader = csv.reader(input_stream, quoting=csv.QUOTE_NONNUMERIC)
    for row_num, row in enumerate(spamreader):  # row is List of string
        if row_num == 0:
            header = row
        else:
            records.append(row)
    return header, records


def facilities_with_max_value_by_column_index(records, col_index):
    # TODO: validate parameter values, raise exception if bad
    best_performers = []
    if not records:
        print('records list is empty', file=sys.stderr)
    else:
        max_rate = max(record[col_index] for record in records)
        best_performers = [record for record in records if record[col_index] == max_rate]
    return best_performers


def facilities_with_max_value_from_stream(input_stream, column_name):
    # TODO: validate parameter values, raise exception if bad
    header, records = read_csv_stream(input_stream)
    col_index = column_index(column_name, header)
    return facilities_with_max_value_by_column_index(records, col_index)


def column_index(column_name, header):
    # TODO: validate parameter values, raise exception if bad
    return header.index(column_name)


def facilities_with_max_value(filepath, column_name):
    # TODO: validate parameter values, raise exception if bad
    with open(filepath, newline='') as input_stream:
        return facilities_with_max_value_from_stream(input_stream, column_name)


def facilities_with_max_value_hard_to_test(filepath, column_name):
    # TODO: validate parameter values, raise exception if bad
    with open(filepath, newline='') as input_stream:
        records = []
        spamreader = csv.reader(input_stream, quoting=csv.QUOTE_NONNUMERIC)
        for row_num, row in enumerate(spamreader):  # row is List of string
            if row_num == 0:
                header = row
            else:
                records.append(row)
        col_index = header.index(column_name)
        max_rate = max(record[col_index] for record in records)
        best_performers = [record for record in records if record[col_index] == max_rate]
    return best_performers
