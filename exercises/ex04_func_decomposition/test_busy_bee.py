"""
Unit tests for Busy Bee word game application.
"""

from pytest import mark

from busy_bee import BusyBee


class TestBusyBee:
    def setup_method(self, method):
        self.busy_bee = BusyBee()

    def test_find_all_words_one_letter_success(self):
        letters = 'i'
        words = self.busy_bee.find_all_words(letters)
        assert words == ['i']

    def test_find_all_words_one_letter_failure(self):
        letters = 'x'
        words = self.busy_bee.find_all_words(letters)
        assert words == []

    def test_find_all_words_three_letters_all_results_max_len_success(self):
        letters = 'but'
        words = self.busy_bee.find_all_words(letters)
        assert set(words) == set(['but', 'btu', 'bu', 'bt', 'tb', 'tu', 'tub', 'ut'])

    def test_find_all_words_three_letters_results_different_lengths_success(self):
        letters = 'cat'
        words = self.busy_bee.find_all_words(letters)
        assert set(words) == set(['a', 'at', 'act', 'ca', 'ct', 'cat', 'ta', 'tc'])

    def test_find_all_words_seven_letters_success(self):
        letters = 'tadflow'

        all_words = self.busy_bee.find_all_words(letters)

        assert set(all_words).issuperset(set(
            ['a', 'ado', 'aft', 'aloft', 'alto', 'at', 'awl', 'daft', 'do',
             'dot', 'dolt', 'fad', 'flat', 'float', 'flow', 'fowl', 'lad',
             'loaf', 'lot', 'low', 'loft', 'oaf', 'oat', 'oft', 'old', 'owl',
             'tad', 'tao', 'toad', 'told', 'tow', 'two', 'waft', 'wold',
             'wolf']
        ))
