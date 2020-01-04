"""
Busy Bee word game module.
"""


class BusyBee:
    """ Busy Bee game solver """

    # TODO: find better word list. words.txt has too many abbreviations, etc.

    def __init__(self):
        self.words = set()
        with open('words.txt') as word_file:
            for word in word_file:
                self.words.add(word.strip())

    def find_all_words(self, letters):
        """
        Return a list of all English words that can be formed from the given string of letters
        """
        return [perm for perm in self.all_permutations(letters)
                if perm in self.words]

    def all_permutations(self, letters):
        """
        Recursive function to return a list of strings that are all
        permutations of the given letters
        """
        if not letters:  # condition to stop recursion
            return []
        else:
            first_letter = letters[0]
            other_letters = letters[1:]
            # recursive call to the current method.
            # make sure the argument is shorter than the current call's
            # argument so we'll eventually get to the stop condition.
            permutations_of_other_letters = self.all_permutations(other_letters)
            # add the first letter by itself to the other permutations.
            new_permutations = [first_letter] + permutations_of_other_letters
            # for each of the other permutations, create new permutations by
            # inserting our first_letter at every position
            for permutation in permutations_of_other_letters:
                for i in range(0, len(permutation) + 1):
                    new_permutations.append(
                        permutation[:i] + first_letter + permutation[i:])
            return new_permutations
