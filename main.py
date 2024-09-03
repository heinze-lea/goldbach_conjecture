# external
import numpy as np
import matplotlib.pyplot as plt

# custom
from prime_functions import (
    sieve_of_erathosthenes,
    count_primes_in_nto2n,
    pi_of_n,
    symmetric_prime_number_distances,
)

# ##### PARAMS ######

compute_primes = False
plot_distances = False
saving_figs = False
lim = 500000
n_lim = int(lim/2)

######################


# <editor-fold desc="Calculate / Load prime numbers">
if compute_primes:
    prime_numbers = sieve_of_erathosthenes(lim, 'artifacts/primes/prime_100000.npy')
    np.save(f'artifacts/primes/prime_{str(lim)}.npy', prime_numbers)

else:
    prime_numbers = np.load(f'artifacts/primes/prime_{str(lim)}.npy')
# </editor-fold>


# Calculate pi(n) -> derive pi(2n) - pi(n) from there
count_primes = pi_of_n(lim, prime_numbers)


# Calculate pi(2n) - pi(n)
# TODO: put in count_primes_in_nto2n
ns = range(int(lim/2))
count_primes_n_to_2n = [count_primes[2*i] - count_primes[i] for i in ns]

# <editor-fold desc="Plot pi(2n) - pi(n)">
# Plot prime numbers between n and 2n with increasing n
x = ns
y = count_primes_n_to_2n

a, b = np.polyfit(x, y, 1)
# (np.float64(0.07661473506079812), np.float64(580.8583839413034))
# R2 = 0.99

plt.plot(x, y, 'b', label='data')
plt.plot(x, a*x+b, '--k', label=f"fit: y={str(round(a, 2))}*x + {round(b, 2)}")
plt.xlabel('n')
plt.ylabel('number of primes between n and 2n')
plt.title('Prime count between n and 2n with increasing n')
plt.legend()
plt.savefig(f'artifacts/plots/prime_count_nto2n.png')
plt.show()
# </editor-fold> (

# TODO: Plot pi(2n) / pi(n)


# <editor-fold desc="Calculate / Plot symmetric distances to prime numbers (i) over n">
if plot_distances:
    distances_to_primes = []

    for n in range(2, n_lim):
        distances_to_primes.append(symmetric_prime_number_distances(n, prime_numbers))

    # plot number of distances per n
    count_distances = [len(dists) for dists in distances_to_primes]
    plt.scatter(range(2, n_lim), count_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('number of symmetric distances from n to 2 prime numbers')
    plt.title('Count of symmetric prime distances')
    plt.savefig(f'artifacts/plots/n_distances.png')
    plt.show()

    # plot minimal distance per n
    min_distances = [min(dists) for dists in distances_to_primes]
    plt.scatter(range(2, n_lim), min_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('minimal symmetric distance from n to 2 prime numbers')
    plt.title('Minimal symmetric prime distance')
    plt.savefig(f'artifacts/plots/min_distance.png')
    plt.show()

    #histogram of minimal distance
    plt.hist(min_distances, bins=100)
    plt.show()

    # plot maximal distance per n

    max_distances = [max(dists) for dists in distances_to_primes]
    plt.scatter(range(2, n_lim), max_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('maximal symmetric distance from n to 2 prime numbers')
    plt.title('Maximal symmetric prime distance')
    plt.savefig(f'artifacts/plots/max_distance.png')
    plt.show()

    #histogram of maximal distance
    plt.hist(max_distances, bins=100)
    plt.show()
# </editor-fold>

