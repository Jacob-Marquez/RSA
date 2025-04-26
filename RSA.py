import random
from math import gcd

# Miller-Rabin primality test
def isPrime(n, k=20):
    
    if n < 2: return False
    
    # small primes check to save time
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
        
    # n-1 = d * 2^s
    d = n-1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
        
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for __ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

# Generates a random prime of length "digits"
def generatePrime(digits):
    # set range of numbers
    low = 10**(digits-1)
    high = 10**digits - 1
    while True:
        # pick a random candidate in [low, high]
        p = random.randrange(low, high)
        if p % 2 == 0:
            p += 1
        # test only odd numbers
        while p < high:
            # Miller-Rabin primality test
            if isPrime(p):
                return p
            p += 2

# Extended Euclidean Algorithm
# Returns (x,y,g) where a*x + b*y = g, g is the gcd
def extendedEEA(a, b):
    if b == 0:
        return (1, 0, a)
    x, y, g = extendedEEA(b, a % b)
    return (y, x - (a//b)*y, g)

# Modular Exponentiation through exponentiation by squaring
def modExp(x, a, n):
    x = x % n
    z = 1
    while a > 0:
        if a & 1:
            z = (x * z) % n
        x = (x * x) % n
        a >>= 1
    
    return z

# Generates private and public keys then writes to txt files
def genKeys(p, q):
    n = p * q
    phi = (p-1)*(q-1)

    # choose e
    e = 65537
    
    # In case 65537 does not work for e
    if gcd(e, phi) != 1:
        e = 3

    # compute d = e^(-1) mod phi
    x, y, g = extendedEEA(e, phi)
    d = x % phi

    # write keys and n to text files
    with open('public_key.txt', 'w') as f:
        f.write(f"{n}\n{e}\n")

    with open('private_key.txt', 'w') as f:
        f.write(f"{n}\n{d}\n")
        
    print(f"n :{n}")
    print(f"phi: {phi}")
    print(f"pub key: {e}")
    print(f"priv: {d}")
        
def encrypt():
        # read public key
    with open('public_key.txt') as f:
        n = int(f.readline().strip())
        e = int(f.readline().strip())

    # read message
    with open('message.txt') as f:
        m = int(f.read().strip())

    # encrypt ciphertext = (plaintext^e) mod n
    c = pow(m, e, n)

    # write ciphertext
    with open('ciphertext.txt', 'w') as f:
        f.write(str(c))
        
    print(f"orignal message: {m}")
    print(f"ciphertext: {c}")
        
    return
        
def decrypt():

    # read private key
    with open('private_key.txt') as f:
        n = int(f.readline().strip())
        d  = int(f.readline().strip())

    # read ciphertext
    with open('ciphertext.txt') as f:
        c = int(f.read().strip())

    # decrypt plaintext = (ciphertext^d) mod n
    m = pow(c, d, n)

    # write decrypted message
    with open('decrypted_message.txt', 'w') as f:
        f.write(str(m))
        
    print(f"decrypted message: {m}")
        
    return
    
def main():
    
    # generate p and q of length 100, with a difference ≥ 10^95
    
    while True:
        p = generatePrime(100)
        q = generatePrime(100)
        if p != q and abs(p-q) >= pow(10, 95):
            break

    genKeys(p,q)
    
    encrypt()
    
    decrypt()
    

if __name__ == '__main__':
    main()