import math
# get message, turn each into 3 digit ascii, combine into one number and add 1s then RSA
from time import time
from numba import jit
import os


pepper = "IAMSUPERMAN"


@jit(nopython=True)
def modInverse(e, phi):
    for d in range(2, phi):
        if (d*e) % phi ==1:
            return d



@jit(nopython=True)
def coprime(phi):
    #finds a number that is coprime to the euler totient function
    #finds e

    for e in range(2, phi):
        if math.gcd(e, phi) ==1:
            return e


class ENCRYPTOR:
    def __init__(self):
        self.e = None
        self.d = None
        self.n = None
        self.genKeys()


    def printStatus(self,):
        print("Generating keys" + "." * (math.ceil(time())%4))
        os.system('cls')




    def genKeys(self, p=7919, q=1009):
        self.printStatus()
        p = 100109 #7919
        q = 100057 #1009

        self.n = p*q
        phi = (p-1)*(q-1)


        self.e = coprime(phi)

        self.d = modInverse(self.e, phi)

        print( "(e, n)", self.e , self.n)
        print("(d, n)", self.d, self.n)

    def encrypt(self, message ):
        return pow(message, self.e, self.n)

    def decrypt(self, message ):
        return pow(message, self.d, self.n)

    #RSA
    def superman(self, message):
        l = list(message)
        encrypted = [self.encrypt(ord(x)) for x in l]
        return encrypted

    # UN-RSA
    def kryptonite(self, messageList):
        m = [chr(self.decrypt(x)) for x in messageList]
        return "".join(m)


print(pow(8191216381, 8191216381))