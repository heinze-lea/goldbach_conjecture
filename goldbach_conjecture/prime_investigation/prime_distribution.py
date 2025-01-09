# external
import numpy as np
import matplotlib.pyplot as plt

# custom
from goldbach_conjecture.utils.prime_functions import (
    sieve_of_erathosthenes,
    pi_of_n,
    gauss_pi_n,
    count_primes_in_nto2n,
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
