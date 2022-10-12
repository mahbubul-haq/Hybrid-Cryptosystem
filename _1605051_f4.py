import random
import math
from _1605051_f5 import bigmod
import time
import _1605051_f5

def mod_inverse(a, m):

    def gcd_extended_euclid(a, b, x, y):
        if a == 0:
            x[0] = 0
            y[0] = 1
            return b
        x1 = [0]
        y1 = [0]
        gcd = gcd_extended_euclid(b % a, a, x1, y1)
        x[0] = y1[0] - (b // a) * x1[0]
        y[0] = x1[0]
        return gcd

    x = [0]
    y = [0]
    g = gcd_extended_euclid(a, m, x, y)
    assert (g == 1)
    res = (x[0] % m + m) % m
    return res

def two_K_bit_primes(K):

    def check_composite(n, a, d, s):
        x = bigmod(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for i in range(1, s):
            x = x * x % n
            if x == n - 1:
                return False
        return True

    def miller_rabin(n, iter):
        if n < 4:
            return n == 2 or n == 3
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        for i in range(iter):
            a = random.randint(2, n - 2)
            if check_composite(n, a, d, s):
                return False
        return True

    prime_check_start = 2 ** (K - 1) + 1
    primes = []

    while len(primes) < 2:

        possibly_prime = True
        for i in range(3, 100, 2):
            if prime_check_start % i == 0:
                flag = False
                break

        if possibly_prime:
            if miller_rabin(prime_check_start, 100):
                primes.append(prime_check_start)

        prime_check_start += 2

    return primes

def get_rsa_keys(K):

    primes = two_K_bit_primes(K)

    n = primes[0] * primes[1]
    phi = (primes[0] - 1) * (primes[1] - 1)
    e = 2
    while math.gcd(phi, e) != 1:
        e += 1

    d = mod_inverse(e, phi)
    public_e_n = [e, n]
    private_d_n = [d, n]

    return [public_e_n, private_d_n]

def rsa_encrypt(key, plaintext):

    encrypted_data = [_1605051_f5.bigmod(ord(i), key[0], key[1]) for i in plaintext]
    return encrypted_data

def rsa_decrypt(key, encrypted_data):
    decrypted_data = ''.join([chr(_1605051_f5.bigmod(i, key[0], key[1])) for i in encrypted_data])
    return decrypted_data


if __name__ == "__main__":

    plain_text = input("Enter Plain text: ")

    k = [16, 32, 64, 128]

    sample_output = []

    print("K".ljust(5) + "Key-Generation(ms)".center(20) + "Encryption(ms)".center(15) + "Decryption(ms)".center(15))

    for i in k:
        start = time.time()
        keys = get_rsa_keys(i // 2)

        key_generation = time.time() - start
        start = time.time()
        encrypted_data = rsa_encrypt(keys[0], plain_text)
        encryption_time = time.time() - start
        start = time.time()
        decrypted_data = rsa_decrypt(keys[1], encrypted_data)
        decryption_time = time.time() - start
        print(str(i).ljust(5) + str(round(key_generation * 1000, 10)).center(20) + str(round(encryption_time * 1000, 10)).center(15) + str(round(decryption_time * 1000, 10)).center(15))
        #print(decrypted_data == plain_text)

        if i == 32:
            sample_output.append({'public': tuple(keys[0]), 'private': tuple(keys[1])})
            sample_output.append(encrypted_data)
            sample_output.append(decrypted_data)

    print("\nGenerated keys: ")
    print(sample_output[0])
    print("\nCipher Text:")
    print(sample_output[1])
    print("\nDecrypted Text:")
    print(sample_output[2])




