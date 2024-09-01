import numpy as np
from time import time


def sieve_of_erathosthenes(
    n_end: int,
    file_first_primes: str == '',
) -> np.array:

    """
    Returns list of prime numbers which can be found from 2 on up until a certain number.

    :param n_end: End number until to look for prime numbers
    :param file_first_primes: npy file containing prime numbers which have been found in a smaller number interval range, also expected to be starting at 2.
    :return: numpy array of prime numbers in [2, n_end]
    """

    # no first primes given
    if file_first_primes == '':
        all_numbers = list(range(2, n_end))
        start_index_offset = 0

    # load first prime numbers and complete numbers set for undiscovered prime area
    else:
        first_primes = list(np.load(file_first_primes))
        all_numbers = first_primes + list(range(first_primes[-1]+1, n_end))

        # dont have to investigate the first primes which have already been confirmed
        start_index_offset = len(first_primes)-1

    # for every prime
    for i, prime in enumerate(all_numbers):

        offset = i if i >= start_index_offset else start_index_offset

        # check all other numbers that follow and delete them from set if they divide by prime
        # not dividing prime by itself
        for n in all_numbers[offset+1:]:
            if n % prime == 0:
                j = all_numbers.index(n)
                all_numbers.pop(j)

    return np.array(all_numbers)


def count_primes_in_nto2n(n: int, primes: np.array) -> int:

    """
    Calculate how many prime numbers can be found in [n, 2n].

    :param n: n in [n, 2n] interval
    :param primes: list of prime numbers known for an interval > [2, 2n]
    :return: number of primes in [n, 2n]
    """
    return len(primes[(primes>=n) & (primes<2*n)])


def symmetric_prime_number_distances(n: int, primes: np.array) -> np.array:

    """
    Calculate at which equal distances from n prime numbers can be found in both directions. If n is a prime number, then 0 is also returned as one possible distance.
    :param n: number for evaluation
    :param primes: list of prime numbers known for an interval > [2, 2n]
    :return: list of distances. if a distance i is found, then n+i and n-i are both prime numbers. Goldbach conjecture poses that this list is never empty for any n.
    """

    #start_time = time.time()

    primes_low = primes[primes <= n]
    distances_to_low_prime_numbers = n - primes_low

    primes_high = primes[(primes >= n) & (primes < 2*n)]
    distances_to_high_prime_numbers = primes_high - n

    prime_ind = sorted(list(set(distances_to_low_prime_numbers).intersection(set(distances_to_high_prime_numbers))))
    #end_time = time.time()
    #delta_time = end_time - start_time

    # to check
    #all_numbers = np.arange(1, 2 * n)
    #possible_sum_pairs = np.array([all_numbers[:n][::-1], all_numbers[n-1:]]).T
    #possible_sum_pairs[prime_ind] -> all pairs of prime numbers that sum up to 2n

    return prime_ind