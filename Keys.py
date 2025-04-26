import random
from math import gcd

def is_prime(n, k=20):
    """Miller–Rabin primality test."""
    if n < 2: return False
    # small primes check
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = d * 2^s
    d, s = n-1, 0
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

def generate_prime(digits):
    """Generate a random prime of exactly `digits` decimal digits."""
    low = 10**(digits-1)
    high = 10**digits - 1
    while True:
        # pick a random candidate in [low, high]
        p = random.randrange(low, high)
        if p % 2 == 0:
            p += 1
        # test only odd numbers
        while p < high:
            if is_prime(p):
                return p
            p += 2

def extended_gcd(a, b):
    """Return (x, y, gcd) such that a*x + b*y = gcd."""
    if b == 0:
        return (1, 0, a)
    x, y, g = extended_gcd(b, a % b)
    return (y, x - (a//b)*y, g)

def main():
    # 1) generate p, q of 100 decimal digits, difference ≥ 10**95
    digits = 100
    while True:
        p = generate_prime(digits)
        q = generate_prime(digits)
        if p != q and abs(p-q) >= 10**95:
            break

    n = p * q
    phi = (p-1)*(q-1)

    # 2) choose e
    e = 65537
    if gcd(e, phi) != 1:
        # fallback if unlucky
        e = 3

    # 3) compute d = e^(-1) mod phi
    x, y, g = extended_gcd(e, phi)
    d = x % phi

    # 4) write keys
    with open('public_key.txt', 'w') as f:
        f.write(f"{n}\n{e}\n")

    with open('private_key.txt', 'w') as f:
        f.write(f"{n}\n{d}\n")

if __name__ == '__main__':
    main()