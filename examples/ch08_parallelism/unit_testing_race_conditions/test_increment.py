import unittest

import before_after

from unit_testing_race_conditions import db, increment


class TestIncrmnt(unittest.TestCase):
    def setUp(self):
        db.reset_db()

    def test_increment(self):
        increment.increment()

        count = db.get_count()
        self.assertEqual(count, 1)

    def test_sequential_increment(self):
        increment.increment()
        increment.increment()

        count = db.get_count()
        self.assertEqual(count, 2)

    def test_increment_race(self):
        with before_after.after('increment.db.get_count', increment.increment):
            increment.increment()

        count = db.get_count()
        self.assertEqual(count, 1)  # Should be 2

    def test_locking_increment_race(self):
        def erroring_locking_increment():
            # Trying to get a lock when the other thread has it will cause a
            # CouldNotLock exception - catch it here or the test will fail
            with self.assertRaises(db.CouldNotLock):
                increment.locking_increment()

        with before_after.after(
                'increment.db.get_count', erroring_locking_increment):
            increment.locking_increment()

        count = db.get_count()
        self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
