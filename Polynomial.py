from random import random

__author__ = 'Aaron Blumenfeld'

# This is an implementation of a polynomial mod 2. I used sets
# instead of lists for possible sparse polynomials. Sets
# are used instead of Dictionaries since we're working mod 2: if a degree is in the
# underlying data structure, the only possible value would be 1.

# You should enter polynomials in terms of z. E.g., z^2 + z + 1. Use lower case z.
# You can also enter coefficients in front of the z. E.g., 3z. But these coefficients
# will get reduced mod 2.

class Polynomial:

    def __init__(self, s = "0"):
        self._poly = set()
        s = s.replace(" ", "") # remove spaces
        split = s.split("+") # split into list of monomials
        for i in range(len(split)):
            val = Polynomial.parseMonomial(split[i])
            if val != -1:
                if val not in self._poly:
                    self._poly.add(val)
                else:
                   self._poly.remove(val)

    def degree(self):
        max = -1 # deg(0) = -1
        for i in self._poly:
            if i > max:
                max = i
        return max

    def __eq__(self, other):
        pTerms = 0
        for i in self._poly:
            pTerms += 1
        qTerms = 0
        for i in other._poly:
            qTerms += 1
        if pTerms != qTerms:
            return False
        for i in self._poly:
            if i not in other._poly:
                return False
        return True

    def __add__(self, q):
        rval = Polynomial()
        for i in self._poly: # loop through terms in p polynomial
            if i not in q._poly:
                rval._poly.add(i)
        for i in q._poly: # loop through terms in q polynomial
            if i not in self._poly:
                rval._poly.add(i)
        return rval

    def multHelper(self, i): # computes p -> z^i*p
        if i < 0:
            raise ValueError("Only use nonnegative values for i!")
        rval = Polynomial()
        for j in self._poly:
            rval._poly.add(i+j)
        return rval

    def __mul__(self, q):
        rval = Polynomial()
        for i in self._poly: # applies distributive law
            rval += q.multHelper(i)
        return rval

    def __mod__(self, q):
        rval = Polynomial(str(self))
        pmax = rval.degree()
        qmax = q.degree()

        while pmax >= qmax:
            rval += q.multHelper(pmax-qmax)
            pmax = rval.degree()
        return rval

    def modExp(self, k, q):
        temp = Polynomial(str(self))
        rval = Polynomial("1")
        while k > 0:
            if k % 2 == 1:
                rval = (rval * temp) % q
            k //= 2
            temp = (temp * temp) % q
        return rval

    def inverse(self, q): # p^(ord-1) = 1 by Lagrange's Theorem, so p^(ord-2) = p^(-1)
        if self == Polynomial(): # 0 is not invertible
            return None
        return self.modExp((1 << q.degree()) - 2, q)

    def sqrt(self, q):
        m = q.degree()
        return self.modExp(1 << (m-1), q)

    def __str__(self):
        if len(self._poly) == 0:
            return "0"
        rval = ""
        a = list(self._poly)
        a = sorted(a, reverse = True)
        n = len(a)
        for i in range(n):
            if a[i] > 1:
                rval += "z^" + str(a[i]) + " "
            elif a[i] == 1:
                rval += "z "
            else: # i == 0
                rval += "1 "
            if i < n-1:
                rval += "+ "
        rval = rval.strip()
        return rval

    @staticmethod
    def generatePolys(polys):
        if len(polys) == 0: # generate list [0, 1]
            polys.append(Polynomial("0"))
            polys.append(Polynomial("1"))
        else: # generate list of polynomials of degree <= n from list of polynomials of degree <= n-1
            l = []
            for i in range(len(polys) // 2, len(polys)):
                temp = polys[i].multHelper(1)
                l.append(temp)
                temp += Polynomial("1")
                l.append(temp)
            polys += l

    @staticmethod
    def random(n): # returns random polynomial of max degree n
        p = Polynomial()
        for i in range(n+1):
            if(random() > 0.5):
                p += Polynomial("z^" + str(i))
        return p

    @staticmethod
    def isValid(s):
        if len(s) == 0:
            return True
        lastType = -1 # 0 corresponds to z, 1 corresponds to ^, 2 corresponds to number, 3 corresponds to +
        c = s[0]
        if c == 'z':
            lastType = 0
        elif c >= '0' and c <= '9':
            lastType = 2
        else:
            return False

        for i in range(1, len(s)):
            c = s[i]
            if c == 'z':
                if lastType != 2 and lastType != 3:
                    return False
                lastType = 0
            if c == '^':
                if lastType != 0:
                    return False
                lastType = 1
            if c >= '0' and c <= '9':
                if lastType == 0:
                    return False
                lastType = 2
            if c == '+':
                if lastType != 0 and lastType != 2:
                    return False
                lastType = 3
        return True


    @staticmethod
    def parseMonomial(s):
        if len(s) > 0:
            c = s[0]
            if c == 'z':
                if len(s) == 1:
                    return 1
                else:
                    return int(s[2 : len(s)])
            if c >= '0' and c <= '9':
                zIndex = s.find('z')
                if zIndex != -1:
                    coeff = int(s[0 : zIndex]) % 2
                    if s.find('^') == -1: # if we see nz
                        if coeff != 0:
                            return 1
                    else: # if we see nz^i
                        if coeff != 0:
                            return int(s[zIndex + 2 : len(s)])
                if zIndex == -1 and int(s) % 2 == 1:
                    return 0
        return -1 # 0 polynomial

def main():
    p = Polynomial("z^4 + z^3 + z^2 + z")
    print(p)
    q = Polynomial("z^2 + z + 1")
    print(q)
    print(p + q)
    print(p * q)
    print(str(p % q) + "\n")

    print("random " + str(Polynomial.random(5)))
    print(Polynomial("z^2").inverse(Polynomial("z^4 + z + 1")))

    p = Polynomial("z^3")
    print(p)

    p = Polynomial("1")
    print(p)

    print(Polynomial() == Polynomial())
    print(Polynomial())

    p = Polynomial("z^2 + z + z + 1 + z^3 + z^2")
    print(p)
    print(Polynomial.isValid("3z"))

    p = Polynomial("z^3 + z^2")
    print(p.sqrt(Polynomial("z^4 + z + 1")))

    p = Polynomial("z^2 + 1")
    q = Polynomial("z")
    print(p % q)

#main()