import unittest
import numpy as np

from goldbach_conjecture.utils.prime_functions import (
    sieve_of_erathosthenes,
    pi_of_n,
    gauss_pi_n,
    count_primes_in_nto2n,
    symmetric_prime_number_distances,
    find_prime_twins,
    prime_twins_in_symmetric_distances,
)


class PrimeFunctionTests(unittest.TestCase):
    prime_end = 50
    prime_numbers_50 = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
    prime_twins_50 = np.array([3, 5, 7, 11, 13, 17, 19, 29, 31, 41, 43])
    prime_density_function_50 = np.array([
        0, 0, 0, 1, 2, 2, 3, 3, 4, 4,
        4, 4, 5, 5, 6, 6, 6, 6, 7, 7,
        8, 8, 8, 8, 9, 9, 9, 9, 9, 9,
        10, 10, 11, 11, 11, 11, 11, 11, 12, 12,
        12, 12, 13, 13, 14, 14, 14, 14, 15, 15,
    ])


    def test_sieve(self):
        # prime numbers until 50
        np.testing.assert_array_equal(self.prime_numbers_50, sieve_of_erathosthenes(self.prime_end))

    def test_pi_n(self):
        # prime number density until 50
        np.testing.assert_array_equal(self.prime_density_function_50, pi_of_n(self.prime_end, self.prime_numbers_50))
        # prime number density until 30
        np.testing.assert_array_equal(self.prime_density_function_50[:30], pi_of_n(30, self.prime_numbers_50))

    def test_gauss_pi(self):
        # test for n = 2
        np.testing.assert_array_equal(np.array([0, 0]), gauss_pi_n(2))
        # test for n > 2
        gauss_approx = gauss_pi_n(self.prime_end)
        self.assertEqual(gauss_approx[40], 40.0/np.log(40.0))

    def test_count_primes_nto2n(self):
        # make some point tests
        test_numbers = [4, 10, 15, 24]
        primes_between_n_2n = [2, 4, 4, 6]

        # based on pi_n
        primes_artifact = {'pi_n': self.prime_density_function_50}
        prime_count_array = count_primes_in_nto2n(int(self.prime_end/2), primes_artifact)

        [self.assertEqual(primes_between_n_2n[i], prime_count_array[n]) for i, n in enumerate(test_numbers)]

        # based on primes
        primes_artifact = {'primes': self.prime_numbers_50}
        prime_count_array = count_primes_in_nto2n(int(self.prime_end / 2), primes_artifact)
        [self.assertEqual(primes_between_n_2n[i], prime_count_array[n]) for i, n in enumerate(test_numbers)]

        # based on unexpected Keyword
        primes_artifact = {'prime_list': self.prime_numbers_50}
        self.assertRaises(
            NotImplementedError,
            count_primes_in_nto2n,
            int(self.prime_end / 2),
            primes_artifact,
        )

    def test_symmetric_distances(self):
        # test symmetric distances from 15
        output = symmetric_prime_number_distances(15, self.prime_numbers_50)
        np.testing.assert_array_equal(np.array([2, 4, 8]), output)

        # test low distances
        np.testing.assert_array_equal(np.array([]),  symmetric_prime_number_distances(1, self.prime_numbers_50))
        np.testing.assert_array_equal(np.array([0]),  symmetric_prime_number_distances(2, self.prime_numbers_50))

    def test_find_twins(self):
        # test prime twins
        np.testing.assert_array_equal(self.prime_twins_50, find_prime_twins(self.prime_numbers_50))

    def test_prime_twins_in_symmetric_pairs(self):
        distances = [[], [], [0], [0], [], [], [], [], [], [], [], [], [], [], [], [2, 4, 8]]

        # for n = 15
        n = 15
        self.assertEqual((5, 5.0/6.0), prime_twins_in_symmetric_distances(n, distances, self.prime_twins_50))

        n = 2
        self.assertEqual((0, 0), prime_twins_in_symmetric_distances(n, distances, self.prime_twins_50))

        n = 3
        self.assertEqual((1, 1), prime_twins_in_symmetric_distances(n, distances, self.prime_twins_50))
