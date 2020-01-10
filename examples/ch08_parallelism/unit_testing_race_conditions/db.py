from contextlib import contextmanager

db = {}

COUNT = 'count'
LOCK = 'lock'


def reset_db():
    db.clear()

    # initialise count to 0
    db[COUNT] = 0


def get_count():
    return db[COUNT]


def set_count(val):
    db[COUNT] = val


class CouldNotLock(Exception):
    pass


@contextmanager
def get_lock():
    if LOCK in db:
        raise CouldNotLock()
    db[LOCK] = True
    yield
    db.pop(LOCK)
