RC = [0x0000000000000001,
      0x0000000000008082,
      0x800000000000808A,
      0x8000000080008000,
      0x000000000000808B,
      0x0000000080000001,
      0x8000000080008081,
      0x8000000000008009,
      0x000000000000008A,
      0x0000000000000088,
      0x0000000080008009,
      0x000000008000000A,
      0x000000008000808B,
      0x800000000000008B,
      0x8000000000008089,
      0x8000000000008003,
      0x8000000000008002,
      0x8000000000000080,
      0x000000000000800A,
      0x800000008000000A,
      0x8000000080008081,
      0x8000000000008080,
      0x0000000080000001,
      0x8000000080008008]

r = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]
b = 1600
rate = 1088
l = 6
rounds = 12 + 2 * l


def rot(a, n):
    return ((a << (n % 64)) + (a >> (64 - (n % 64)))) % (1 << 64)


def roundB(A):
    for i in range(0, 24):
        D = [0, 0, 0, 0, 0]
        C = [0, 0, 0, 0, 0]
        B = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

        for x in range(5):
            for y in range(5):
                D[x] ^= A[x][y]
        for x in range(0, 5):
            C[x] = D[(x + 4) % 5] ^ rot(D[(x + 1) % 5], 1)
        for x in range(0, 5):
            for y in range(0, 5):
                A[x][y] ^= C[x]
        for x in range(0, 5):
            for y in range(0, 5):
                B[y][(2 * x + 3 * y) % 5] = rot(A[x][y], r[x][y])
        for x in range(0, 5):
            for y in range(0, 5):
                A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])
        A[0][0] ^= RC[i]
    return A


def padding(M):
    q = rate - (len(M) * 8 % rate)  # count of bits depends on hash length
    if q == 0:
        M.append(l)
        for i in range(1, rate // 8 - 1):
            M.append(0x00)
        M.append(0x80)
    elif q == 8:
        M.append(l ^ 0x80)
    elif q == 16:
        M.append(l)
        M.append(0x80)
    else:
        M.append(l)
        for i in range(1, q // 8 - 1):
            M.append(0x00)
        M.append(0x80)
    return M


def keccak(M):
    blocksNum = (len(M) * 8) // rate
    state = []
    for idn in range(0, blocksNum):
        blockBytes = M[idn * (rate // 8):(idn + 1) * rate // 8]
        block = []
        for i in range(0, rate // 8, 8):
            block.append(int.from_bytes(blockBytes[i:i + 8], byteorder='little', signed=False))
        for i in range(rate // 8, b // 8, 8):
            block.append(0)
        block = [block[i:21 + i:5] for i in range(0, 5)]
        if idn != 0:
            for i in range(0, 5):
                for j in range(0, 5):
                    state[i][j] ^= block[i][j]
        else:
            state = block
        state = roundB(state)
    return state


def hash(A):
    M = padding(A)
    state = keccak(M)
    return printHash(state)


def printHash(state):
    res = 0
    for i in range(4):
        res |= state[i][0] << (64 * i)
    return res.to_bytes(32, byteorder='little').hex()


def calculateHash(filename):
    file = open(filename, 'rb')
    A = bytearray(file.read())
    return hash(A)
