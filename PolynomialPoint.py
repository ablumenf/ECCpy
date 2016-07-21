from Polynomial import Polynomial

__author__ = 'Aaron Blumenfeld'

# The following program implements point addition and multiplication
# for elliptic curves. Lopez-Dahab (LD) projective coordinates are used, not affine.
# Therefore, to understand the points, (1 : 0 : 0) represents the point
# at infinity; otherwise, the z-coordinate is 1, and (x : y : z)
# represents (x/z, y/z^2) in affine coordinates. But the toString method prints
# either (x, y) or the string "infinity".

class PolynomialPoint:

    def __init__(self, x=Polynomial("1"), y=Polynomial(), z=Polynomial()):
        self._x = x
        self._y = y
        self._z = z

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getZ(self):
        return self._z

    def setX(self, x):
        self._x = x

    def setY(self, y):
        self._y = y

    def setZ(self, z):
        self._z = z

    def __eq__(self, Q):
        return self._x == Q.getX() and self._y == Q.getY() and self._z == Q.getZ()

    def __str__(self):
        if self == PolynomialPoint():
            return "infinity"
        return "(" + str(self._x) + ", " + str(self._y) + ")"

    # uses LD projective coordinates formulas from Guide to Elliptic Curve Cryptography
    # this method separate so add method isn't as messy
    def addHelper(self, Q, a, b, modulus):
        infinity = PolynomialPoint()
        if Q == infinity: # if Q = infinity ==> P + Q = P
            return self
        if self == infinity: # if P = infinity ==> P + Q = Q
            return Q
        if PolynomialPoint(self.getX() % modulus, self.getY() % modulus, self.getZ() % modulus) == Q: # point doubling
            z3 = self.getX() * self.getX()
            temp = self.getZ() * self.getZ()
            z3 *= temp
            x3 = self.getX() * self.getX()
            x3 *= x3
            temp = self.getZ() * self.getZ()
            temp *= temp
            temp *= b
            x3 += temp
            y3 = self.getZ() * self.getZ()
            y3 *= y3
            y3 *= b * z3
            temp = (a * z3) + (self.getY() * self.getY()) + (b * self.getZ().modExp(4, modulus))
            temp *= x3
            y3 += temp
            return PolynomialPoint(x3, y3, z3)
        Q.setX(Q.getX() * Q.getZ().inverse(modulus)) # point addition
        temp = Q.getZ() * Q.getZ()
        temp = temp.inverse(modulus)
        Q.setY(Q.getY() * temp)
        Q.setZ(Polynomial("1"))
        A = Q.getY() * self.getZ() * self.getZ()
        A += self.getY()
        B = Q.getX() * self.getZ()
        B += self.getX()
        C = self.getZ() * B
        temp = a * self.getZ() * self.getZ()
        temp += C
        D = B * B * temp
        z3 = C * C
        E = A * C
        x3 = A * A
        x3 += D + E
        F = Q.getX() * z3
        F += x3
        G = Q.getX() + Q.getY()
        G *= z3 * z3
        y3 = E + z3
        y3 *= F
        y3 += G
        return PolynomialPoint(x3, y3, z3)

    def add(self, Q, a, b, modulus):
        rval = self.addHelper(Q, a, b, modulus)
        temp = rval.getZ() % modulus
        if temp != Polynomial(): # z != 0
            rval.setX(rval.getX() * temp.inverse(modulus))
            rval.setX(rval.getX() % modulus)
            temp *= temp
            rval.setY(rval.getY() * temp.inverse(modulus))
            rval.setY(rval.getY() % modulus)
            rval.setZ(Polynomial("1"))
        else: # z = 0
            rval.setX(Polynomial("1"))
            rval.setY(Polynomial())
        return rval

    def mult(self, k, a, b, modulus): # compute kP using repeated doubling
        A = k
        B = PolynomialPoint()
        C = PolynomialPoint(self.getX(), self.getY(), self.getZ())
        while A > 0:
            if A % 2 == 0: # if A is even
                A //= 2
                C = C.add(C, a, b, modulus)
                C.setX(C.getX() % modulus)
                C.setY(C.getY() % modulus) # reduce to prevent huge-degree polynomials
                C.setZ(C.getZ() % modulus)
            else: # if A is odd
                A -= 1
                B = B.add(C, a, b, modulus)
                B.setX(B.getX() % modulus)
                B.setY(B.getY() % modulus) # reduce to prevent huge-degree polynomials
                B.setZ(B.getZ() % modulus)
        return B

def main():
    x = Polynomial("z^3")
    y = Polynomial("1")
    z = Polynomial("1")
    a = Polynomial("z^3")
    b = Polynomial("z^3 + 1")
    m = Polynomial("z^4 + z + 1")
    P = PolynomialPoint()
    Q = PolynomialPoint(x, y, z)
    for i in range(1, 23):
        P = P.add(Q, a, b, m)
        print("" + str(i) + " " + str(P))
        print("" + str(i) + " " + str(Q.mult(i, a, b, m)))

    P = PolynomialPoint(Polynomial("z^3+z^2"), Polynomial("z^3+z^2"), Polynomial("1"))
    Q = PolynomialPoint(Polynomial("z^3+1"), Polynomial("z^3+z^2+z+1"), Polynomial("1"))
    R = P.add(Q, a, b, m)
    print(R)
    print(R.getZ())

#main()