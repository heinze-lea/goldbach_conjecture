## Building a prime number classification model

### Version 1: Logistic Regression with Feature Exploration
We want to start with the easiest version possible:
- logistic regression with a small set of features, classifying all numbers < 500000 as prime / not prime

The challenge lies here in the definition of meaningful features. 
Trivially, features can reflect modularity of prime numbers ( = is number n dividable by 2, 3, 5, ...). 
One can make up endless many of such modular features, and using them in high extend reduces
the classification to a simple problem of linear combination as it is actually solvable whether a number is prime.

<br>
Non-modular features could refer to the last prime seen, the number of primes seen so far etc. It 
is currently in progress which such kind of features whose information content is meaningful enough to help the classification problem.
Goal is that the logistic model only partially relies on modular features and uses non-modular features as well, without
introducing too much noise.

