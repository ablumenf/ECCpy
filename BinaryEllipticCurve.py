import math
from Polynomial import Polynomial
from PolynomialPoint import PolynomialPoint

__author__ = 'Aaron Blumenfeld'

# The following program implements elliptic curves. Non-supersingular elliptic
# curves over binary fields are of the form y^2 + xy = x^3 + ax^2 + b.  They have
# no repeated roots on the right side of the equation, which is
# equivalent to b != 0. The isEC method tests if a given equation is an elliptic
# curve or not. Point and curve orders, logarithms, and lists of points are
# implemented. There are also static methods for generating
# lists of elliptic curves.

# No methods exist for finding elliptic curves of prime order since these curves
# over binary fields always have an even number of points. Indeed, the inverse of
# a point (x, y) is (x, x + y). In particular, the inverse of (0, y) is (0, y). Thus
# if (0, y) is on the curve, we have a subgroup of order 2. (0, y) is on the curve
# iff y^2 = b has a solution. But it turns out that every element of the finite field
# F_(2^r) has a square root, so there is always a point on the curve of the form (0, y).
# One constructive way to see this is that b^(2^r-1) = 1 by Lagrange's Theorem, so
# b^(2^r) = (b^(2^(r-1)))^2 = b.

# There are also supersingular elliptic curves over binary fields. These have the form
# y^2 + cy = x^3 + ax + b. I have not implemented these. Although these can be interesting
# to study, it is known that discrete logarithms on supersingular elliptic curves over F_q can
# be solved by transformation into discrete logarithms in F_(q^k) for fairly small k. For this
# reason, supersingular elliptic curves are typically avoided in cryptography.

# The logarithm calculator just uses brute force. Perhaps in the future I'll
# implement something like Pollard-Rho.

# You are responsible for making sure the irreducible polynomial you use is actually irreducible.
# The default, z^32 + z^26 + z^23 + z^22 + z^16 + z^11 + z^10 + z^8 + z^7 + z^5 + z^4 + z^2 + z + 1,
# is irreducible.

class BinaryEllipticCurve:

    def __init__(self, a, b, modulus):
        self._a = a
        self._b = b
        self._modulus = modulus

    def getA(self):
        return self._a

    def getB(self):
        return self._b

    def getModulus(self):
        return self._modulus

    def setA(self, a):
        self._a = a

    def setB(self, b):
        self._b = b

    def setModulus(self, modulus):
        self._modulus = modulus

    def __str__(self):
        t = "E(F_(2^" + str(self.getModulus().degree()) + ")) : "
        s = "y^2 + xy = x^3"
        if self._a != Polynomial():
            s += " + (" + str(self._a) + ")x^2"
        if self._b != Polynomial():
            s += " + (" + str(self._b) + ")"
        return t + s

    def isEC(self):
        b = self.getB()
        return b != Polynomial() # make sure no multiple roots

    def order(self): # O(q^2) algorithm, where q = 2^r
        polys = []
        for i in range(self.getModulus().degree()):
            Polynomial.generatePolys(polys)
        count = 1 # point at infinity
        for i in range(len(polys)):
            for j in range(len(polys)):
                leftside = (polys[j] * polys[j] + polys[i] * polys[j]) % self.getModulus() # y^2 + xy
                rightside = (polys[i] * polys[i] * polys[i] + self.getA() * polys[i] * polys[i] + self.getB())\
                            % self.getModulus() # x^3 + ax^2 + b
                if leftside == rightside:
                    count += 1
        return count

    def pointOrder(self, G):
        a = self.getA()
        b = self.getB()
        modulus = self.getModulus()
        temp = 1 << self._modulus.degree()
        N = int(temp + 1 + 2*math.sqrt(temp)) # use max possible order to avoid quadratic time in computing the curve order
        P = PolynomialPoint()
        infinity = PolynomialPoint()
        for i in range(1, N+1):
            P = P.add(G, a, b, modulus)
            if P == infinity:
                return i
        return -1 # error

    def log(self, P, G): # return k, where kG = P
        temp = 1 << self._modulus.degree()
        N = int(temp + 1 + 2*math.sqrt(temp)) # use max possible order to avoid quadratic time in computing the curve order
        B = PolynomialPoint() # B = infinity
        for i in range(1, N+1):
            B = G.add(B, self.getA(), self.getB(), self.getModulus())
            if B == P:
                return i
        return -1 # error

    def listRandomPoints(self, n):
        count = 0
        s = ""
        a = self.getA()
        b = self.getB()
        modulus = self.getModulus()
        deg = modulus.degree()
        while count < n:
            foundPoint = False
            while not foundPoint:
                x = Polynomial.random(deg-1)
                y = Polynomial.random(deg-1)
                leftside = (y*y + x*y) % modulus
                rightside = (x*x*x + a*x*x + b) % modulus
                if leftside == rightside:
                    foundPoint = True
            s += str(PolynomialPoint(x, y, Polynomial("1"))) + "\n"
            count += 1
        s += str(count) + " points were generated.\n"
        return s

    @staticmethod
    def listRandomECs(m, irred, n):
        if (m & (m-1)) != 0: # only powers of 2 don't have this property
            return "" + str(m) + " is not a power of 2."
        count = 0
        rval = ""
        deg = int(math.log(m, 2))
        while count < n:
            a = Polynomial.random(deg-1)
            b = Polynomial.random(deg-1)
            E = BinaryEllipticCurve(a, b, irred)
            if E.isEC():
                rval += str(E) + "\n"
                count += 1
        rval += str(count) + " curves were generated.\n"
        return rval

def main():
    E = BinaryEllipticCurve(Polynomial("z^3"), Polynomial("z^3 + 1"), Polynomial("z^4 + z + 1"))
    print(E.order())
    print(str(E) + "\n")
    print(E.listRandomPoints(10))

    irr = Polynomial("z^20 + z^19 + z^18 + z^17 + z^16 + z^15 + z^14 + z^13 + z^12 + z^11 + z^10 + z^9 + z^8 + z^7 +"
                     " z^6 + z^4 + z^4 + z^3 + 1")
    print(BinaryEllipticCurve.listRandomECs(1024 * 1024, irr, 10))

    G = PolynomialPoint(Polynomial("z^3"), Polynomial("1"), Polynomial("1"))
    print(E.pointOrder(G))

    P = PolynomialPoint(Polynomial("z^3 + z + 1"), Polynomial("z"), Polynomial("1"))
    print(E.log(P, G))

#main()