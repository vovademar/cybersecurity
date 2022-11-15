import math
import rabin_miller
import random
import keccak
import rsa.core as core


def generate_keypair(key_size: int = 1024) -> (tuple[int, int, int, int], tuple[int, int]):
    p = rabin_miller.generate_large_prime(key_size)
    q = rabin_miller.generate_large_prime(key_size)

    n = p * q
    euler = (p - 1) * (q - 1)

    while True:
        e = random.randrange(pow(2, key_size - 1), pow(2, key_size))
        if math.gcd(e, euler) == 1:
            break

    # modular inverse
    d = pow(e, -1, euler)
    return (p, q, n, d), (n, e)


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
    keys = generate_keypair()
    private_key = keys[0]
    public_key = keys[1]
    a = 123
    encrypt = rsa_encrypt(public_key, a)
    dec = rsa_decrypt(private_key, encrypt)
    print(f'Before encrypt: {a}')
    print(f'After encrypt: {encrypt}')
    print(f'After decrypt: {dec}')
    print(f'Reference: {core.decrypt_int(encrypt, private_key[3], private_key[2])}')


def big_test():
    print('Big test')
    keys = generate_keypair()
    private_key = keys[0]
    public_key = keys[1]
    fileHash = keccak.calculateHash('file')
    a = int(fileHash, 16)
    encrypt = rsa_encrypt(public_key, a)
    dec = rsa_decrypt(private_key, encrypt)
    print(f'Hash before encrypt: {fileHash}')
    print(f'After encrypt: {encrypt}')
    print(f'Hash after decrypt: {hex(dec)[2:]}')
    reference = core.decrypt_int(encrypt, private_key[3], private_key[2])
    print(f'Reference: {hex(reference)[2:]}')


simple_test()
big_test()
