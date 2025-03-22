import numpy as np
from time import time


def sieve_of_erathosthenes(
    n_end: int,
    file_first_primes: str = '',
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


def pi_of_n(n: int, primes: np.array) -> np.array:

    """
    Returning an n-length array containing prime number density for every integer < n.

    :param n: n, threshold for array length
    :param primes: list of prime numbers
    :return: array with index i, containing number of primes < i
    """
    # naive implementation, one could do more elegantly, but run time is so not an issue rn
    return np.array([len(primes[(primes<i)]) for i in range(n)])


def gauss_pi_n(n: int) -> np.array:
    """
    Returning an n-length array containing Gauss-approximated prime number density for every integer < n.

    :param n: n, threshold for array length
    :return: array with index i, containing number of primes < i
    """

    # x = 0 and x = 1 return inf, but prime distribution is only meaningful from 2 onwards
    if n > 2:
        return np.array([0, 0] + [x/np.log(x) for x in range(2, n)])
    else:
        return np.zeros(n)


def count_primes_in_nto2n(n: int, primes_artifact: dict) -> list:

    """
    Calculate how many prime numbers can be found in [n, 2n].

    :param n: cutoff n
    :param primes_artifact: dict with list referring to prime number lists. can either be a list of prime numbers
    ('primes') or the cumulative prime number distribution ('pi_n')
    :return: array with index i, containing number of primes in [i, 2i]
    """

    artifact_keys = list(primes_artifact.keys())

    if 'pi_n' in artifact_keys:
        count_primes = primes_artifact['pi_n']
        return [count_primes[2 * i] - count_primes[i] for i in range(n)]

    # except that "pi_n" is not in prime_artifact dictionary
    elif 'primes' in artifact_keys:
        primes = primes_artifact['primes']
        return [len(primes[(primes >= i) & (primes < 2*i)]) for i in range(n)]

    else:
        raise NotImplementedError("Dictionary primes_artifact neither contains list of primes nor list of prime densities.")


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


def find_prime_twins(primes: np.array) -> np.array:
    """
    Calculates prime numbers which are part of a prime number twin pair.
    :param primes: array of prime numbers
    :return: array of prime number twins
    """
    prime_twin_start = (primes[1:] - primes[:-1]) == 2
    # rotate array by one
    prime_twin_end = np.roll(prime_twin_start, 1)
    prime_twin_end[0] = False

    # might be useful: array which is true if prime is part of a prime twin pair
    # prime_twin_bool = prime_twin_start | prime_twin_end
    # actual prime twins
    prime_twins = primes[:-1][prime_twin_start | prime_twin_end]
    return prime_twins


def prime_twins_in_symmetric_distances(n: int, distances: list, prime_twins: np.array) -> tuple:

    """
    Find the number of prime twins in all n+i / n-i prime pairs for the distances i and the natural number n.
    :param n: Natural number n
    :param distances: Distances i so that n+i and n-i are both primes
    :param prime_twins: All prime twins < 2n
    :return number of prime twins and number of prime twins in relation to number of n+i/n-i primes:
    """
    if n > 1:
        # get prime distances
        n_distances = distances[n]
        # convert prime distances to prime numbers involved in distances
        dist_primes = [o for d in n_distances for o in [n - d, n + d]]
        dist_primes_set = set(dist_primes)    # if n is prime, n occurs twice as dist_prime
        # filter down to prime twins
        prime_twins_in_distances = dist_primes_set.intersection(set(prime_twins))
        # return absolute and relative prime abundance
        return len(prime_twins_in_distances), len(prime_twins_in_distances)/len(dist_primes_set)
    else:
        return None, None
