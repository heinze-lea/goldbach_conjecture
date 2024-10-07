## Analysing the Goldbach Conjecture

### Background



**Goldbach Conjecture**

Every even number is the sum of 2 prime numbers.  <br>

$$ 2n = p_1 + p_2 $$

**Remarks:**
- there can be more than one pair of prime numbers to sum up to n
- $p_1$ and $p_2$ can be equal

<br>
A different perspective of the problem would be

$$ 2n = (n - i) + (n + i) $$

which means: for every natural number n, there exists at least one distance i in [0, n), so that n+i and n-i are both prime numbers.

The Goldbach Conjecture is demonstrated up to very large numbers, but remains to be mathematically proven.


### Investigation

We start heuristically to extend our naive understanding of the prime number distribution.
(One can of course dive directly into the Riemann Zeta Function, but thats the focus yet.)

**1. Prime numbers between n and 2n** <br>
The prime number distribution pi(n) typically is defined by the total number of primes smaller than n. pi(n)
is known to be monotonously increasing and diverging to $\inf$. <br>
In addition, we can explore the number of primes between n and 2n for any natural n. The Goldbach Conjecture
suggests, that there always has to be a prime number between n and 2n, so that n+i can be prime for at least one i<n.
If we find that the number of primes between n & 2n is decreasing with higher n, that could be a first indicator that
Goldbach Conjecture might be wrong.

*Result* <br>
The number of primes between n and 2n is continuously growing, and that with an almost linear shape, which is super interesting.
One can continue the investigation by checking this function for higher primes (maybe its slope decreases with higher n)
and by mathematically exploring whether the Gauss heuristic for pi(n) would also predict such a linear function for #primes(n, 2n)

<br> <br>

**2. Symmetric prime distance i** <br>
The Goldbach Conjecture poses that there should be at least one i for any n so that n+i and n-i are primes, but in reality,
there is often more than only one possible solution to i. It is interesting to explore:
- the number of i found with increasing n
- the maximum and minimum value of i
