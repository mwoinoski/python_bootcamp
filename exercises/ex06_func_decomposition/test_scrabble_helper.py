"""
Unit tests for Scrabble Helper word game application.
"""
# pylint: disable=unused-argument,attribute-defined-outside-init
# pylint: disable=missing-class-docstring,missing-function-docstring

from scrabble_helper import ScrabbleHelper


class TestScrabbleHelper:
    def setup_method(self, method):
        self.scrabble_helper = ScrabbleHelper()

    def test_find_all_words_one_letter_success(self):
        letters = 'i'
        words = self.scrabble_helper.find_all_words(letters)
        assert words == ['i']

    def test_find_all_words_one_letter_failure(self):
        letters = 'x'
        words = self.scrabble_helper.find_all_words(letters)
        assert words == []

    def test_find_all_words_three_letters_all_results_max_len_success(self):
        letters = 'but'
        words = self.scrabble_helper.find_all_words(letters)
        assert set(words) == {'but', 'tub', 'ut'}

    def test_find_all_words_three_letters_results_diff_lengths_success(self):
        letters = 'cat'
        words = self.scrabble_helper.find_all_words(letters)
        assert set(words) == {'a', 'at', 'act', 'cat', 'ta'}

    def test_find_all_words_seven_letters_success(self):
        letters = 'tadflow'

        all_words = self.scrabble_helper.find_all_words(letters)

        assert set(all_words).issuperset({
            'a', 'ado', 'aft', 'aloft', 'alto', 'at', 'awl', 'awol', 'daft',
            'do', 'dot', 'dolt', 'fad', 'flat', 'float', 'flaw', 'fat', 'foal',
            'fold', 'flow', 'fowl', 'lad', 'law', 'load', 'loaf', 'lot', 'low',
            'loft', 'of', 'oaf', 'oat', 'oft', 'old', 'owl', 'tad', 'to',
            'tao', 'toad', 'told', 'tow', 'two', 'wad', 'waft', 'wold', 'wolf'
        })
