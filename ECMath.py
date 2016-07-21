from random import randint

__author__ = 'Aaron Blumenfeld'

# This program implements various functions for math
# operations used throughout the ECC Toolkit. This
# includes modular inverses, square roots, Jacobi (Legendre)
# symbols, primality testing, and factoring. Factoring uses
# Pollard-Rho for O(sqrt(p)) time complexity.

def inverse(a, p): # lazy way to compute a^(-1) (mod p)
    if a == 0:
        return -1; # indicates error
    return pow(a, p-2, p)

def sqrt(a, p): # Shanks' algorithm for sqrt(a) (mod p)
    if a % p == 0: # sqrt(0) = 0
        return 0
    if p % 4 == 3: # easy for p = 3 (mod 4)
        return pow(a, (p+1)//4, p)
    if p % 8 == 5 and pow(a, (p-1)//4, p) == 1: # sometimes easy for p = 5 (mod 8)
        return pow(a, (p+3)//8, p)
    e = 0
    q = p-1
    while q % 2 == 0 and q > 0:
        e += 1
        q //= 2
    n = 2
    while jacobi(n, p) != -1:
         n = randint(0, p-1)
    z = pow(n, q, p)
    y = z
    r = e
    x = pow(a, (q-1)//2, p)
    b = (a * x * x) % p
    x = (a * x) % p
    while b % p != 1:
        m = 0
        while pow(b, 1 << m, p) != 1:
            m += 1
        t = pow(y, 1 << (r-m-1), p)
        y = (t * t) % p
        r = m
        x = (x * t) % p
        b = (b * y) % p
    return x

def jacobi(a, p):
    if a % p == 0:
        return 0
    rval = 1
    a = a % p

    while a != 0:
        while a % 2 == 0: # pull out factors of 2 and compute (2/n)
            a //= 2
            mod8 = p % 8
            if mod8 == 3 or mod8 == 5:
                if rval == 1:
                    rval = -1
                else:
                    rval = 1
        temp = a
        a = p # swap a and p
        p = temp

        if a % 4 == 3 and p % 4 == 3: # apply quadratic reciprocity
            if rval == 1:
                rval = -1
            else:
                rval = 1
        a = a % p
    return rval

def isPrime(N):
    if N == 0 or N == 1:
          return False
    if N == 2:
        return True
    if N % 2 == 0:
        return False
    s = N-1
    while s % 2 == 0: # write N-1 = 2^k*s
        s //= 2
    for i in range(50): # 50 iterations has failure rate of <= 1/2^100
        a = randint(1, N-1)
        exp = s
        mod = pow(a, exp, N)
        while exp != N-1 and mod != 1 and mod != N-1:
            mod = (mod * mod) % N
            exp *= 2
        if mod != N-1 and exp % 2 == 0:
            return False
    return True

def randomPrime(n):
    rval = 0
    while not isPrime(rval):
        rval = randint(pow(10, n-1), pow(10, n)-1)
        if rval <= 3: # want p >= 5
            rval = 0
    return rval

def gcd(a, b):
    while b > 0:
        temp = b
        b = a % b
        a = temp
    return a

def f(x, a, b):
    return a*x*x + b

def findFactor(n):
    maxiterssq = 0.7854*n # pi/4 * n
    x = randint(1, n-1)
    y = x
    d = 1
    iters = 0
    a = randint(1, n-1)
    b = randint(1, n-1)
    while d == 1 or d == n: # a match should be found within sqrt(pi*n/2) iterations on average
        if iters*iters > maxiterssq: # otherwise, choose a new function f (we may be running into a k-cycle if d == n)
            a = randint(1, n-1)
            b = randint(1, n-1)
            x = randint(1, n-1)
            y = x
            iters = 0
        x = f(x, a, b) % n
        y = f(f(y, a, b), a, b) % n
        d = gcd(abs(x-y), n)
        iters += 1
    return d

def findPrimeFactor(n, factors):
    if isPrime(n):
        factors.append(n)
    else:
        temp = n // findFactor(n)
        findPrimeFactor(temp, factors)

def factor(n, factors):
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    while n % 3 == 0:
        factors.append(3)
        n //= 3
    while n > 1:
        findPrimeFactor(n, factors)
        n //= factors[-1]

def findAllFactors(primeFactors, allFactors):
    if len(primeFactors) == 0:
        allFactors.append(1)
    elif len(allFactors) == 0:
        allFactors.append(1)
        allFactors.append(primeFactors[0])
    for i in range(1, len(primeFactors)):
        temp = []
        for f in allFactors:
            if f * primeFactors[i] not in allFactors:
                temp.append(f * primeFactors[i])
        allFactors += temp
    allFactors.sort()

def allFactors(N): # uses Pollard Rho
    factors = []
    factor(N, factors)
    allFactors = []
    findAllFactors(factors, allFactors)
    return allFactors

def main():
    print(allFactors(1200))
    for i in range(17):
        print(jacobi(i*i*i + 2*i + 2, 17))
    for i in range(100, 200):
        print(str(i) + " " + str(isPrime(i)))
    print(randomPrime(4))

#main()