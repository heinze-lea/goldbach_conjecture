# external
import numpy as np
import matplotlib.pyplot as plt

# custom
from goldbach_conjecture.utils.prime_functions import (
    sieve_of_erathosthenes,
    pi_of_n,
    gauss_pi_n,
    count_primes_in_nto2n,
    symmetric_prime_number_distances,
    find_prime_twins,
    prime_twins_in_symmetric_distances,
)

# ##### PARAMS ######

compute_primes = False
plot_distances = False
saving_figs = False
lim = 500000
n_lim = int(lim/2)

######################

prime_artifacts = {}

# <editor-fold desc="Calculate / Load prime numbers">
if compute_primes:
    primes = sieve_of_erathosthenes(lim, '../../artifacts/primes/prime_100000.npy')
    np.save(f'artifacts/primes/prime_{str(lim)}.npy', primes)

else:
    primes = np.load(f'artifacts/primes/prime_{str(lim)}.npy')
# </editor-fold>

prime_artifacts['primes'] = primes


### Investigate prime number distribution and its approximations ###

# Calculate pi(n) -> derive pi(2n) - pi(n) from there
prime_artifacts['pi_n'] = pi_of_n(lim, prime_artifacts['primes'])    # pi_n: cumulative prime number distribution

# Calculate and store Gauss approximation of pi_n
# choosing higher lim for Gauss approx as it does not depend on finding prime numbers
prime_artifacts['gauss_pi_n'] = gauss_pi_n(lim*10)

# Calculate pi(2n) - pi(n)
count_primes_n_to_2n = count_primes_in_nto2n(n_lim, prime_artifacts)

# Calculate pi(2n) / pi(n)
pi_2n_division = [prime_artifacts['pi_n'][2 * i] / prime_artifacts['pi_n'][i] for i in range(n_lim)]

# <editor-fold desc="Plot all pi(n) distributions">
fig, ax, = plt.subplots(2, 2, figsize=(12, 12))

# pi(n)
ax[0, 0].plot(range(lim), prime_artifacts['pi_n'], 'b', label='pi(n)')
ax[0, 0].plot(range(lim), prime_artifacts['gauss_pi_n'][:lim], '--r', label='Gauss approx')
ax[0, 0].set_xlabel('n')
ax[0, 0].set_ylabel('pi(n)')
ax[0, 0].set_title('Prime count distribution pi(n)')
ax[0, 0].legend()
#ax[0, 0].set_xticklabels(ax[0, 0].get_xticks(), rotation=50)

# pi(2n) - pi(n)
x = range(n_lim)
y = count_primes_n_to_2n
a, b = np.polyfit(x, y, 1)
# (np.float64(0.07661473506079812), np.float64(580.8583839413034))
# R2 = 0.99
y_theo = [prime_artifacts['gauss_pi_n'][2*i] - prime_artifacts['gauss_pi_n'][i] for i in range(n_lim)]
ax[0, 1].plot(x, y, 'b', label='pi(2n) - pi(n)')
ax[0, 1].plot(x, a*x+b, '--k', label=f"fit: y={str(round(a, 2))}*x + {round(b, 2)}")
ax[0, 1].plot(x, y_theo, '--r', label='Gauss approx')
ax[0, 1].set_xlabel('n')
ax[0, 1].set_ylabel('pi(2n) - pi(n)')
ax[0, 1].set_title('Investigate prime distribution: \n pi(2n) - pi(n)')
ax[0, 1].legend()
#ax[0, 1].set_xticklabels(ax[0, 1].get_xticks(), rotation=50)


# pi(2n) / pi(n)
x = range(n_lim)
y = pi_2n_division
y_theo = [prime_artifacts['gauss_pi_n'][2*i] / prime_artifacts['gauss_pi_n'][i] for i in range(n_lim)]
ax[1, 0].plot(x, y, 'b', label='pi(2n)/pi(n)')
ax[1, 0].plot(x, y_theo, 'r', label='Gauss approx')
ax[1, 0].set_xlabel('n')
ax[1, 0].set_ylabel('pi(2n) / pi(n)')
ax[1, 0].set_title('Investigate prime distribution: \n pi(2n) / pi(n)')
ax[1, 0].legend()
#ax[1, 0].set_xticklabels(ax[1, 0].get_xticks(), rotation=50)

# Gauss approx for very high numbers
ax[1, 1].plot(range(len(prime_artifacts['gauss_pi_n'])), prime_artifacts['gauss_pi_n'], '--r', label='Gauss approx')
ax[1, 1].set_xlabel('n')
ax[1, 1].set_ylabel('approximated pi(n)')
ax[1, 1].set_title('Gauss approximated \n prime count distribution pi(n)')
ax[1, 1].legend()
#ax[1, 1].set_xticklabels(ax[1, 1].get_xticks(), rotation=50)

plt.subplots_adjust(wspace=0.3, hspace=0.5)
plt.savefig(f'artifacts/plots/pi_n_distribution.png', bbox_inches='tight') #if saving_figs else None
# plt.show()
plt.close()
# </editor-fold>


### Investigate symmetric distance i which leads to prime numbers n+i & n-i for any n ###

# Calculate symmetric distances i to prime numbers
n_lim_distances = 50000
distances_to_primes = [symmetric_prime_number_distances(n, prime_artifacts['primes']) for n in range(n_lim_distances)]

# <editor-fold desc="Plot symmetric distances to prime numbers (i) over n">
if plot_distances:

    # plot number of distances per n
    count_distances = [len(dists) for dists in distances_to_primes]
    plt.scatter(range(n_lim_distances), count_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('number of symmetric distances from n to 2 prime numbers')
    plt.title('Count of symmetric prime distances')
    plt.savefig(f'artifacts/plots/symmetric_distance/n_distances.png') if saving_figs else None
    plt.show()

    # lets look deeper into these # symmetric distances
    # it seems like there is a sharp boundary for the min -> is that true or just a side effect of the visualization?
    # -> NO
    plt.plot(range(n_lim_distances), count_distances, 'x')
    plt.xlabel('n')
    plt.ylabel('number of symmetric distances from n to 2 prime numbers')
    plt.title('Count of symmetric prime distances')
    plt.ylim(0, 260)
    plt.xlim(6000, 10000)
    plt.savefig(f'artifacts/plots/symmetric_distance/zoom_n_distances.png') if saving_figs else None
    plt.show()

    # plot minimal distance per n
    min_distances = [min(dists) for dists in distances_to_primes]
    plt.scatter(range(n_lim_distances), min_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('minimal symmetric distance from n to 2 prime numbers')
    plt.title('Minimal symmetric prime distance')
    plt.savefig(f'artifacts/plots/symmetric_distance/min_distance.png') if saving_figs else None
    plt.show()

    #histogram of minimal distance
    plt.hist(min_distances, bins=100)
    plt.show()

    # plot maximal distance per n

    max_distances = [max(dists) for dists in distances_to_primes]
    plt.scatter(range(n_lim_distances), max_distances, s=0.2)
    plt.xlabel('n')
    plt.ylabel('maximal symmetric distance from n to 2 prime numbers')
    plt.title('Maximal symmetric prime distance')
    plt.savefig(f'artifacts/plots/symmetric_distance/max_distance.png') if saving_figs else None
    plt.show()

    #histogram of maximal distance
    plt.hist(max_distances, bins=100)
    plt.show()
# </editor-fold>


### Investigate influence of prime twins of symmetric distance i ###

# Calculate prime twins
prime_twins = find_prime_twins(primes)

# <editor-fold desc="Plot symmentric distances only with prime twins">
# plot distances only with prime twins
# -> plot without any correlation
n_twin_lim = 100000
distances_to_twin_primes = [symmetric_prime_number_distances(n, prime_twins) for n in range(n_twin_lim)]

count_twin_distances = [len(dists) for dists in distances_to_twin_primes]
plt.plot(range(n_twin_lim), count_twin_distances, 'x')
plt.xlabel('n')
plt.ylabel('number of symmetric distances from n to 2 prime numbers')
plt.title('Count of symmetric prime distances')
plt.savefig(f'artifacts/plots/prime_twins/n_distances_only_twins.png') #if saving_figs else None
plt.show()
# </editor-fold>


# <editor-fold desc="Plot prime twin abundance in symmetric prime pairs">
prime_twin_abundance = [prime_twins_in_symmetric_distances(n, distances_to_primes[:2*n], prime_twins[prime_twins<2*n])
                        for n in range(10000)]

prime_twin_abundance = np.array(prime_twin_abundance)
prime_twin_abundance = prime_twin_abundance.T
np.save(f'../../artifacts/primes/prime_twin_abundance_in_i_10000.npy', prime_twin_abundance)

fig, ax = plt.subplots(1,2, figsize=(12,5))
p1 = ax[0].scatter(np.arange(10000), count_distances[:10000], c=prime_twin_abundance[0], s=0.2)
ax[0].set_xlabel('n')
ax[0].set_ylabel('number of symmetric distances from n to 2 prime numbers')
ax[0].set_title('Symmetric prime distances with \n amount of prime twins in prime pairs')
cbar = plt.colorbar(p1)
cbar.ax.set_ylabel('amount of prime twins in prime distance pairs')
#cbar.set_label('amount of prime twins in prime distance pairs')

p2 = ax[1].scatter(range(10000), count_distances[:10000], c=prime_twin_abundance[1], s=0.2)
ax[1].set_xlabel('n')
ax[1].set_ylabel('number of symmetric distances from n to 2 prime numbers')
ax[1].set_title('Symmetric prime distances with \n fraction of prime twins in prime pairs')
cbar = plt.colorbar(p2)
cbar.ax.set_ylabel('density of prime twins in prime distance pairs')

plt.subplots_adjust(wspace=0.4)
plt.savefig(f'artifacts/plots/prime_twins/n_distances_twin_abundance.png') if saving_figs else None
plt.show()
# </editor-fold>
