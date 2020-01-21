"""
pi.py - Example of Python multiprocessing.

Monte Carlo approximation of pi. Here's how it works:
1. Draw a square whose sides have length 2. Area of square = 4.
2. Inscribe a circle with diameter 2 within the square. Area of circle = pi.
3. Now start throwing darts randomly at the square.
If the dart hits are evenly distributed, the ratio of the number of hits inside
the circle to the total number of darts is equal to the ratio of the area of
the circle to the area of the square:
    (hits inside circle) / (number of throws) = pi / 4
4. Multiply both sides of the equation by 4 and you have the value of pi:
    4 * (hits / throws) = pi

The calculation is an example of an Embarrassingly Parallel problem, which
means that it's very easy to break the problem up into separate tasks. Tasks
don't need to coordinate or share data in any way, so there's no need for
inter-process communication, locking, etc. We like Embarrassingly Parallel
problems :)

Monte Carlo is not an efficient strategy. Even with 10**9 samples, the value
of pi produced is accurate only to 5 digits. But we'll keep the number of
samples small so it doesn't take too long to run.

Original version appeared in "Python High Performance Programming", by
Gabriele Lanaro.

This version has modifications to use the concurrent.futures module.
"""

from timeit import timeit
from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
import concurrent.futures
import random

total_samples = 10**6  # total number of calculations


def calculate_one_sample():
    x = random.uniform(-1.0, 1.0)
    y = random.uniform(-1.0, 1.0)
    return 1 if x**2 + y**2 <= 1 else 0
    # Here we chose random values in the range [-1.0, 1.0] to distribute
    # values in a square whose sides have length 2. But we'd get the
    # same result if we looked at the distribution of hits in just one quadrant
    # of the square, for example random.uniform(0, 1). The function
    # random.random() returns numbers in the range [0, 1.0), and it runs
    # faster than random.uniform(). Try replacing random.uniform(-1.0, 1.0)
    # with random.random() and see how that changes the script's performance.


# TODO: note the definition of the pi_serial function, which performs
#       a calculation without using processes or threads. It calls
#       calculate_one_sample() one million times and adds up all the return values.
def pi_serial():
    """Perform the Monte Carlo technique in a serial fashion"""
    hits = 0
    for _ in range(total_samples):
        hits += calculate_one_sample()
    # Or, if you prefer the compact generator expression syntax:
    # hits = sum(calculate_one_sample() for _ in range(total_samples))
    pi = 4.0 * hits/total_samples
    return pi


# TODO: note the definition of the sample_multiple function, which calls
#       calculate_one_sample() 250,000 times and adds up all the return values.
def sample_multiple(chunk_size):
    hits = 0
    for _ in range(chunk_size):
        hits += calculate_one_sample()
    return hits
    # Or, generator expression equivalent:
    # return sum(calculate_one_sample() for _ in range(chunk_size))


# TODO: note the definition of the pi_async function, which calls
#      sample_multiple() with four parallel processes.
def pi_async():
    """
    Divide calculation into 4 chunks and create 4 processes to execute
    each chunk.
    """
    ntasks = 4
    # ntasks = multiprocessing.cpu_count() # number of (virtual) CPU cores
    chunk_size = total_samples // ntasks  # divide work into 4 chunks
    futures = set()

    # TODO: note the `with` statement to use a ProcessPoolExecutor.
    with ProcessPoolExecutor() as executor:
    # with ThreadPoolExecutor(max_workers=ntasks) as executor:
        # TODO Step 2: after running this program and examining the output,
        #      comment out the line above with ProcessPoolExecutor and
        #      uncomment the line with ThreadPoolExecutor. Then run the program
        #      again and note the execution times.

        for _ in range(ntasks):
            # for each loop iteration, use a Process to execute sample_multiple
            # with the argument chunk_size. Save the returned Future in a local variable.
            future = executor.submit(sample_multiple, chunk_size)
            futures.add(future)

    hits = 0
    for future in concurrent.futures.as_completed(futures):
        hits += future.result()

    # note how the value of `hits` is used in the next statement
    # (no code change required)
    pi = 4.0 * hits/total_samples
    return pi


if __name__ == '__main__':
    # TODO: note the calls to pi_async() and pi_serial()
    pi_from_pi_async = pi_async()
    print(f'pi_async() returned {pi_from_pi_async}')

    pi_from_pi_serial = pi_serial()
    print(f'pi_serial() returned {pi_from_pi_serial}')

    time = timeit('pi_async()',
                  setup='from __main__ import pi_async',
                  number=1)
    print(f'pi_async() finished in {time:.3} seconds')

    time = timeit('pi_serial()',
                  setup='from __main__ import pi_serial',
                  number=1)
    print(f'pi_serial() finished in {time:.3} seconds')
