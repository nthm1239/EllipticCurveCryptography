from hashlib import sha256
from sha3 import keccak_256
from sympy import isprime
from fractions import Fraction

class EC():
    def __init__(self, a, b, c, d, prime_number):
        if a == 0:
            raise ValueError("a=0 is forbidden")
        if not isprime(prime_number):
            raise ValueError("{} is not prime!".format(prime_number))

        self.a = a % prime_number
        self.b = b % prime_number
        self.c = c % prime_number
        self.d = d % prime_number
        self.p = prime_number

    def isin(self, pt):
        if pt == 0:
            return True

        x, y = pt[0] % self.p, pt[1]% self.p
        value = y ** 2 - self.a * (x ** 3) - self.b * (x ** 2) - self.c * x - self.d

        if value % self.p == 0:
            return True
        return False

    def sum(self, p, q):
        if not self.isin(p):
            raise ValueError("{} is not in the elliptic curve".format(p))
        if not self.isin(q):
            raise ValueError("{} is not in the elliptic curve".format(q))

        if p == 0:
            return q
        if q == 0:
            return p

        x1, y1 = p[0] % self.p, p[1] % self.p
        x2, y2 = q[0] % self.p, q[1] % self.p

        if x1 != x2:
            x3 = ((self.a ** (self.p - 2) * (y2-y1) ** 2 * (x2-x1) ** (2 * self.p - 4) ) % self.p \
                    - (self.b * self.a ** (self.p - 2)) % self.p\
                    - x1 - x2
                ) % self.p
            y3 = ((-1 * (y2-y1) * (x2-x1) ** (self.p - 2) * x3 ) % self.p \
                + (y2*x1 - y1*x2) * (x2 - x1) ** (self.p - 2) % self.p
                ) % self.p
            return (x3, y3)

        if x1 == x2 and y1 == -1 * y2 % self.p :
            return 0

        if x1 == x2 and y1 != -1 * y2 % self.p:
            x3 = ((4 * self.a * y1 ** 2  % self.p) ** (self.p - 2) % self.p  *\
                  (self.a ** 2  * x1 ** 4 \
                    - 2 * self.a * self.c * x1 ** 2 % self.p\
                    - 8 * self.a * self.d * x1 % self.p
                    - 4 * self.b * self.d % self.p)
            ) % self.p
            y3 = ((8 * self.a * y1 ** 3 % self.p) ** (self.p - 2) % self.p *\
                  (self.a ** 3 * x1 ** 6 % self.p \
                    + 2 * self.a ** 2  * self.b * x1 ** 5 % self.p\
                    + 5 * self.a ** 2 * self.c * x1 ** 4 % self.p \
                    + 20 * self.a ** 2 * self.d * x1 ** 3 % self.p\
                    + (20 * self.a * self.b * self.d % self.p - 5 * self.a * self.c ** 2 % self.p) % self.p * ((x1 ** 2) % self.p) % self.p\
                    + (8 * self.b ** 2 * self.d % self.p - 2 * self.b * self.c ** 2 % self.p - 4 * self.a * self.c * self.d % self.p) * (x1 % self.p) % self.p \
                    + (4 * self.b * self.c * self.d % self.p - 8 * self.a * self.d ** 2 % self.p  - self.c ** 3 % self.p) % self.p )
            ) % self.p

            return (x3, y3)

    def multiple(self, p, n):
        if n == 0:
            return (0, 1)

        q = self.multiple(p, n//2)
        q = self.sum(q, q)

        if n & 1: 
            q = self.sum(q, p)

        return q

# Secp256k1
# https://en.bitcoin.it/wiki/Secp256k1
#a = 0x0000000000000000000000000000000000000000000000000000000000000000
#b = 0x0000000000000000000000000000000000000000000000000000000000000007
#p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
#Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
#Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

a = 0
b = 1
p = 7
Gx = 0
Gy = 1

ell = EC(1,0,a,b,p)
G = (Gx,Gy)
print(ell.isin(G))

pvt_key=3
print(ell.multiple(G,pvt_key))
