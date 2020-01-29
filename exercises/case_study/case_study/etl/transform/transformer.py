"""
Transformation functions for ETL procesing.
"""

from collections import Counter
from datetime import datetime
from enum import Enum, unique
import re
from typing import List, Dict

from case_study.etl.etl_logger import EtlLogger


class Transformer:
    def __init__(self):
        self.logger = EtlLogger()

    def normalize_column_name(self, name: str, max_len: int) -> str:
        """ Return a normalized version of the column name """
        name = name.lower()               # convert to lowercase
        name = re.sub(r'\W', '_', name)   # replace non-word chars with '_'
        name = re.sub(r'__+', '_', name)  # replace multiple '_' with a single '_'
        name = name.strip('_')            # delete leading and trailing '_'
        name = name[:max_len]             # shorten to max_len
        return name

    def count_occurrences(self, cols: List[str]) -> Dict[str, int]:
        """
        Return a dictionary of (column-name, number-of-occurences).
        Assumes the names in the argument list have been normalized.
        """
        return dict(Counter(cols))  # Counter is a dictionary-like object

    def identify_duplicate_columns(self,
            cols: List[str], how_many: Dict[str, int] = None) -> Dict[str, int]:
        """
        Return a dictionary with the name and count of occurrences for each
        duplicate name in the argument `cols`. Names that are not duplicated
        are not present in the returned dictionary.
        """
        if not how_many:
            how_many = self.count_occurrences(cols)
        how_many_dupes_left: Dict[str, int] = {}
        for col in how_many:
            if how_many[col] > 1:
                how_many_dupes_left[col] = how_many[col]
        return how_many_dupes_left

    def make_column_names_unique(self, cols: List[str], max_len: int = 64) -> List[str]:
        """
        Replace duplicate column names with unique names.
        This returned list of unique names perserves the order of the original list
        of names.
        """
        new_cols: List[str] = []

        # add a unique suffix to a column name only if it's duplicated.
        # the requirement to perserve the original order of the list complicates
        # the logic somewhat.
        cols_normalized = [self.normalize_column_name(col, max_len) for col in cols]
        how_many_of_each = self.count_occurrences(cols_normalized)
        how_many_dupes_left: Dict[str, int] = \
            self.identify_duplicate_columns(cols_normalized)

        for col in reversed(cols_normalized):
            suffix: str = ''
            if col in how_many_dupes_left:
                digits = len(str(how_many_of_each[col]))
                num_padded: str = str(how_many_dupes_left[col]).zfill(digits)
                # num_padded: str = f'{dupe_counts[col]:0{digits}}'
                suffix = f'_{num_padded}'
                how_many_dupes_left[col] -= 1
            # if duplicate names have the max len, we need to truncate again before
            # appending the unique suffix
            truncation_pos = max_len - len(suffix)
            new_name: str = f'{col[:truncation_pos]}{suffix}'
            new_cols.insert(0, new_name)

        # Simple solution: add unique suffix to all column names
        # for i, col in enumerate(columns):
        #     suffix: str = f'_{i+1}'
        #     new_col: str = f'{col}{suffix}'
        #     new_columns.append(new_col)

        return new_cols

    @unique
    class DateFormat(Enum):
        """ Valid values for date formats """
        YMD = 1
        MDY = 2
        DMY = 3

    # Date formats in use:
    # YMD: ISO 8601, CN, JP, CA, others
    # DMY: IN, EU, RU, others
    # MDY: US, others
    date_format_patterns: Dict[DateFormat, re.Pattern] = {
        DateFormat.YMD:
            re.compile(r'^(?P<year>\d+)\D(?P<month>\d+)\D(?P<day>\d+)$'),
        DateFormat.MDY:
            re.compile(r'^(?P<month>\d+)\D(?P<day>\d+)\D(?P<year>\d+)$'),
        DateFormat.DMY:
            re.compile(r"""
            ^                # beginning of line
            (?P<day>\d+)     # group named 'day' that captures one or more digits 
            \D               # one non-digit
            (?P<month>\d+)   # group named 'month' that captures one or more digits
            \D               # one non-digit
            (?P<year>\d+)    # group named 'year' that captures one or more digits
            $                # end of line
          """, re.VERBOSE),  # VERBOSE allows whitespace or comments in the pattern
    }

    def get_valid_year(self, year_str: str) -> int:
        """
        Convert year_str to an int in the range 1890 < year < 2150.
        Return 0 if year_str is not a valid 2- or 4-digit year.
        """
        valid_year: int = 0
        if year_str:
            # year must be 2 or 4 digits
            if len(year_str) == 2 or len(year_str) == 4:
                year: int = int(year_str)
                if year >= 0 and (year < 100 or (1890 <= year <= 2150)):
                    if year < 100:
                        year += 2000
                    valid_year = year
        return valid_year

    def normalize_date(self, date: str, date_format: DateFormat = DateFormat.YMD) -> str:
        """
        Normalizes a date string to ISO 8601 format YYYY-MM-DD
        Valid date_format values:
            'YMD' (year-month-day)
            'MDY' (month-day-year)
            'DMY' (day-month-year)
        """
        if date_format not in self.date_format_patterns.keys():
            msg: str = f'invalid date_format value "{date_format}". Valid values' \
                       f'are {list(self.date_format_patterns)}'
            raise ValueError(msg)

        normalized_date: str = ''
        if date:
            date = date.strip()
            pattern = self.date_format_patterns.get(date_format)
            match = pattern.match(date)
            if match:
                year: int = self.get_valid_year(match.group('year'))
                if year:
                    month: int = int(match.group('month'))
                    day: int = int(match.group('day'))
                    # normalized_date = f'{year}-{month:02d}-{day:02d}'
                    try:
                        normalized_date = \
                            datetime(year, month, day).isoformat()[:10]
                    except ValueError:
                        pass
        return normalized_date

    # pylint: disable=line-too-long,W0511
    # TODO: add timezone offset? See https://docs.python.org/3.7/library/datetime.html?highlight=timestamp#datetime.datetime.utcoffset
    def convert_date_to_timestamp(self, date: datetime) -> str:
        """ Return a timestamp string in ISO 8601 format YYYY-MM-DDTHH:MM:SS """
        timestamp: str = ''
        if date:
            date = datetime(date.year, date.month, date.day,
                            date.hour, date.minute, date.second)
            timestamp = date.isoformat()
        return timestamp
