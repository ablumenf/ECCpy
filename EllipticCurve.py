import ECMath
from Point import Point
from random import random
import math

__author__ = 'Aaron Blumenfeld'

# The following program implements elliptic curves. Elliptic
# curves are of the form y^2 = x^3 + ax + b.  They have
# no repeated roots on the right side of the equation, which is
# equivalent to 4a^3 + 27b^2 != 0 (mod p).  The isEC method
# tests if a given equation is an elliptic curve or not.
# Point and curve orders, logarithms, and lists of points are
# implemented. There are also static methods for generating
# lists of elliptic curves.
#
# The logarithm calculator just uses brute force. Perhaps in the future
# I'll implement Pollard's Rho algorithm.

class EllipticCurve:

    def __init__(self, a, b, p):
        self._a = a
        self._b = b
        self._p = p

    def getA(self):
        return self._a

    def getB(self):
        return self._b

    def getP(self):
        return self._p

    def setA(self, a):
        self._a = a

    def setB(self, b):
        self._b = b

    def setP(self, p):
        self._p = p

    def __str__(self):
        t = "E(F_" + str(self._p) + ") : "
        s = "y^2 = x^3 + "
        if self._a == 0:
            pass
        elif self._a == 1:
            s += "x + "
        else:
            s += str(self._a) + "x + "
        s += str(self._b)
        if self._b == 0:
            if self._a == 0:
                s = s[0 : s.index('3') + 1]
            else:
                s = s[0 : s.index('x', 8) + 1]
        return t + s

    def __eq__(self, F):
        return self.order() == F.order()

    def isEC(self):
        a = self.getA()
        b = self.getB()
        p = self.getP()
        return (4*a*a*a + 27*b*b) % p != 0

    def order(self): # O(plogp) algorithm
        a = self.getA()
        b = self.getB()
        p = self.getP()
        order = p + 1
        for x in range(p):
            jac = ECMath.jacobi((x*x*x + a*x + b), p)
            order += jac
        return order

    def pointOrder(self, G):
        factors = ECMath.allFactors(self.order())
        a = self.getA()
        b = self.getB()
        p = self.getP()
        temp = Point(0, 1, 0)
        multiple = 0
        for l in factors:
            temp = temp.add(G.mult(l-multiple, a, b, p), a, b, p)
            multiple = l
            if temp == Point(0, 1, 0):
                return l
        return -1 # error

    def log(self, P, G): # using max possible order (see Hasse's Theorem) as upper bound
        N = int(self._p + 1 + 2*math.sqrt(self._p)) # is faster than computing the exact order first
        B = Point(0, 1, 0)
        for i in range(1, N+1):
            B = G.add(B, self.getA(), self.getB(), self.getP())
            if B == P:
                return i
        return -1 # error

    def listRandomPoints(self, n):
        count = 0
        s = ""
        a = self.getA()
        b = self.getB()
        p = self.getP()
        while count < n:
            x = int(p * random())
            while ECMath.jacobi(x*x*x + a*x + b, p) != 1:
                x = int(p * random())
            y = ECMath.sqrt(x*x*x + a*x + b, p)
            if random() > 0.5:
                y = p - y
            s += str(Point(x, y, 1)) + "\n"
            count += 1
        s += str(count) + " points were generated.\n"
        return s

    @staticmethod
    def listRandomECs(n, p):
        count = 0
        s = ""
        while count < n:
            a = int(p * random())
            b = int(p * random())
            E = EllipticCurve(a, b, p)
            if E.isEC():
                s += str(E) + "\n"
                count += 1
        s += str(count) + " curves were generated.\n"
        return s

    @staticmethod
    def listRandomPrimeECs(n, p):
        count = 0
        s = ""
        while count < n:
            a = int(p * random())
            b = 1 + int((p-1) * random()) # start at 1 since y^2 = x^3 + ax has an even number of points
            E = EllipticCurve(a, b, p)
            order = -1
            if E.isEC():
                order = E.order()
            if order > 0 and ECMath.isPrime(order):
                s += str(E) + ", |E| = " + str(order) + "\n"
                count += 1
        s += str(count) + " curves were generated.\n"
        return s

def main():
    E = EllipticCurve(2, 2, 17)
    print(E)
    print(E.isEC())
    G = Point(5, 1, 1)
    P = Point(0, 6, 1)
    print(E.log(P, G))
    print(E.listRandomPoints(10))
    print(EllipticCurve.listRandomECs(10, 71933))
    E = EllipticCurve(64379, 22921, 71933)
    print(E.listRandomPoints(10))

#main()