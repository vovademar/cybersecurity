import math
import rabin_miller
import random
import keccak


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modularInverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def rsa_generate_keys(key_size: int = 1024) -> (tuple[int, int, int, int], tuple[int, int]):
    if key_size < 1 or key_size % 8 != 0:
        raise Exception('key_size must be positive and multiple by 8')

    p = rabin_miller.generate_large_prime(key_size)
    q = rabin_miller.generate_large_prime(key_size)

    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(pow(2, key_size - 1), pow(2, key_size))
        if math.gcd(e, phi) == 1:
            break

    d1 = modularInverse(e, phi)
    print(f'd1: {d1}')
    # modular inverse
    d2 = pow(e, -1, phi)
    print(f'd1: {d2}')
    # private_key, public_key
    return (p, q, n, d2), (n, e)


def rsa_encrypt(public_key: tuple[int, int], message: int) -> int:
    n = public_key[0]
    e = public_key[1]
    return pow(message, e, n)


def rsa_decrypt(private_key: tuple[int, int, int, int], cipher: int) -> int:
    n = private_key[2]
    d = private_key[3]
    return pow(cipher, d, n)


def simple_test():
    print('Simple test')
    keys = rsa_generate_keys()
    private_key = keys[0]
    public_key = keys[1]

    a = 123
    encrypt = rsa_encrypt(public_key, a)
    dec = rsa_decrypt(private_key, encrypt)
    print(f'Before encrypt: {a}')
    print(f'After encrypt: {encrypt}')
    print(f'After decrypt: {dec}')


def big_test():
    print('Big test')
    keys = rsa_generate_keys()
    private_key = keys[0]
    public_key = keys[1]
    fileHash = keccak.calculateHash('file')
    a = int(fileHash, 16)
    encrypt = rsa_encrypt(public_key, a)
    dec = rsa_decrypt(private_key, encrypt)
    print(f'Hash before encrypt: {fileHash}')
    print(f'After encrypt: {encrypt}')
    print(f'Hash after decrypt: {hex(dec)[2:]}')


simple_test()
big_test()
