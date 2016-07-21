import ECMath

__author__ = 'Aaron Blumenfeld'

# The following program implements point addition and multiplication
# for elliptic curves. Projective coordinates are used, not affine.
# Therefore, to understand the points, (0 : 1 : 0) represents the point
# at infinity; otherwise, the z-coordinate is 1, and (x : y : 1)
# represents (x, y) in affine coordinates. But the __str__ method prints
# either (x, y) or the string "infinity".

class Point:

    def __init__(self, a = 0, b = 1, c = 0):
        self._x = a
        self._y = b
        self._z = c

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
        if self == Point():
            return "infinity"
        return "(" + str(self._x) + ", " + str(self._y) + ")"

    def addHelper(self, Q, a, b, p):
        x3 = 0
        y3 = 0
        z3 = 0
        infinity = Point()
        if self != Q and self != Point(Q.getX(), -Q.getY() % p, Q.getZ()): # if P != +- Q
            u = (Q.getY() * self.getZ() % p) - (self.getY() * Q.getZ() % p)
            v = (Q.getX() * self.getZ() % p) - (self.getX() * Q.getZ() % p)
            w = (u * u * self.getZ() * Q.getZ() % p) - (v*v*v % p) - (2*v*v * self.getX() * Q.getZ() % p)
            x3 = (v*w) % p
            y3 = ((u*(v*v * self.getX() * Q.getZ() - w) % p) - ((v*v*v * self.getY() * Q.getZ()) % p)) % p
            z3 = (v*v*v * self.getZ() * Q.getZ()) % p;
        elif self == Q:
            t = (a * self.getZ() * self.getZ() + 3 * self.getX() * self.getX()) % p
            u = self.getY() * self.getZ() % p
            v = u * self.getX() * self.getY() % p
            w = (t*t - 8*v) % p
            x3 = 2*u*w % p
            y3 = (t * (4*v - w) - 8 * self.getY() * self.getY() * u*u) % p
            z3 = 8*u*u*u % p
        else: # if P = -Q ==> P + Q = infinity
            x3 = 0
            y3 = 1
            z3 = 0
        if self == infinity: # if P = infinity ==> P + Q = Q
            x3 = Q.getX()
            y3 = Q.getY()
            z3 = Q.getZ()
        if Q == infinity: # if Q = infinity ==> P + Q = P
            x3 = self.getX()
            y3 = self.getY()
            z3 = self.getZ()
        return Point(x3, y3, z3)

    def add(self, Q, a, b, p): # call addhelper and reduce coordinates at the end
        R = self.addHelper(Q, a, b, p)
        if R.getZ() % p == 0:
            R.setY(1) # scale infinity down to unique (0, 1, 0)
        else:
            inv = ECMath.inverse(R.getZ(), p)
            R.setX(R.getX() * inv)
            R.setY(R.getY() * inv) # scale z coordinate back down to 1
            R.setZ(R.getZ() * inv)
        R.setX(R.getX() % p)
        R.setY(R.getY() % p) # reduce coordinates mod p
        R.setZ(R.getZ() % p)
        return R

    def mult(self, k, a, b, p): # compute kP using repeated doubling
        A = k
        B = Point()
        C = Point(self.getX(), self.getY(), self.getZ())
        while A > 0:
            if A % 2 == 0: # if A is even
                A //= 2
                C = C.addHelper(C, a, b, p)
                C.setX(C.getX() % p)
                C.setY(C.getY() % p) # reduce mod p O(logk) times to keep integer size down
                C.setZ(C.getZ() % p)
            else: # if A is odd
                A -= 1
                B = B.addHelper(C, a, b, p)
                B.setX(B.getX() % p)
                B.setY(B.getY() % p) # reduce mod p O(logk) times to keep integer size down
                B.setZ(B.getZ() % p)
        if B.getZ() % p == 0:
            B.setY(1) # scale infinity down to unique (0, 1, 0)
        else:
            inv = ECMath.inverse(B.getZ(), p)
            B.setX(B.getX() * inv)
            B.setY(B.getY() * inv) # scale z coordinate back down to 1
            B.setZ(B.getZ() * inv)
        B.setX(B.getX() % p)
        B.setY(B.getY() % p) # reduce coordinates mod p
        B.setZ(B.getZ() % p)
        return B

def main():
    P = Point(5, 1, 1)
    Q = Point(0, 1, 0)
    print(Q)
    for i in range(1, 20):
        Q = Q.add(P, 2, 2, 17)
        print(Q)
    print(P.mult(500, 2, 2, 17))

#main()