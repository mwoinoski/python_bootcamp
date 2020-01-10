from funcy import retry

from unit_testing_race_conditions import db


def increment():
    count = db.get_count()
    new_count = count + 1
    db.set_count(new_count)
    return new_count


def locking_increment():
    with db.get_lock():
        return increment()


def retrying_locking_increment():
    @retry(tries=5, errors=db.CouldNotLock)
    def _increment():
        return locking_increment()

    return _increment()
