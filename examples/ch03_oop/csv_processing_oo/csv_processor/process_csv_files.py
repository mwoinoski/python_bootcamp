"""
Functions to process CSV files.
"""

import csv
import sys


class CsvProcessor:
    def read_csv_file(self, filepath):
        with open(filepath, newline='') as csv_stream:
            return self.process_csv_stream(csv_stream)

    def process_csv_stream(self, input_stream):
        records = []
        row_num = 0
        for line in input_stream:
            if row_num > 0:  # skip header line
                line = line.strip()  # remove newline
                fields = line.split(',')  # fields is a list of strings
                records.append([field.strip('"') for field in fields])
            row_num += 1
        return records
        # return [line.strip().split(',') for line in input_stream][1:]
    
    def process_csv_stream_named_fields(self, input_stream):
        records = []
        row_num = 0
        for line in input_stream:
            if row_num == 0:
                header = line.strip().split(',')
            else:
                fields = line.strip().split(',')  # fields is a list of strings
                record = {}
                for i in range(0, len(header)):
                    column_name = header[i]
                    record[column_name] = fields[i]
                # record = dict(zip(header, fields))
                # record = {header[i]: fields[i] for i in range(0, len(header))}
                records.append(record)
            row_num += 1
        return records
    
    def read_excel_csv_file(self, filepath):
        with open(filepath, newline='') as input_stream:
            return self.read_excel_csv_stream(input_stream)

    def read_excel_csv_stream(self, input_stream):
        records = []
        csv_reader = csv.reader(input_stream, dialect=csv.excel,
                                quoting=csv.QUOTE_NONNUMERIC)
        row_num = 0
        for row in csv_reader:  # row is List of string
            if row_num == 0:
                header = row
            else:
                records.append(row)
            row_num += 1
        return header, records

    def facilities_with_max_value_by_column_index(self, records, col_index):
        best_performers = []
        if not records:
            print('records list is empty', file=sys.stderr)
        else:
            max_rate = max(record[col_index] for record in records)
            best_performers = [record for record in records if record[col_index] == max_rate]
        return best_performers

    def facilities_with_max_value_from_stream(self, input_stream, column_name):
        header, records = self.read_excel_csv_stream(input_stream)
        col_index = self.column_index(column_name, header)
        return self.facilities_with_max_value_by_column_index(records, col_index)

    def column_index(self, column_name, header):
        return header.index(column_name)

    def facilities_with_max_value(self, filepath, column_name):
        with open(filepath, newline='') as input_stream:
            return self.facilities_with_max_value_from_stream(input_stream, column_name)
