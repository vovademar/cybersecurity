
RC = [0x0000000000000001, 0x0000000000008082,
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

def ROTL(x, y):
    return ((x << y) | (x >> (64 - y))) & 0xffffffffffffffff

def KeccakF1600(state):
    for i in range(24):
        C = [state[x] for x in range(0, 25, 5)]
        D = [0, 0, 0, 0, 0]
        for x in range(5):
            D[x] = C[(x + 4) % 5] ^ ROTL(C[(x + 1) % 5], 1)
        for x in range(5):
            for y in range(5):
                state[5 * y + x] ^= D[x]
        B = [0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(5):
            for x in range(5):
                B[0] = state[5 * y + x]
                state[5 * y + x] = ROTL(B[0], r[y][x])
        B = [state[x] for x in range(25)]
        for x in range(25):
            state[x] = B[(x + 3 * ((x + 1) % 5)) % 25] ^ ((~B[(x + 1) % 5]) & B[(x + 2) % 5])
        state[0] ^= RC[i]

def Keccak(bits, input, delimitedSuffix, output):
    rate = 1600 - bits
    blockSize = rate // 8
    S = [0] * 25
    inputOffset = 0
    inputByteLen = len(input)
    while (inputByteLen > rate // 8):
        for i in range(blockSize):
            S[i] ^= input[inputOffset + i]
        KeccakF1600(S)
        inputOffset += blockSize
        inputByteLen -= blockSize
    block = [0] * blockSize
    for i in range(inputByteLen):
        block[i] = input[inputOffset + i]
    block[inputByteLen] = delimitedSuffix
    block[blockSize - 1] |= 0x80
    for i in range(blockSize):
        S[i] ^= block[i]
    if (delimitedSuffix == 0x01):
        KeccakF1600(S)
    for i in range(output // 8):
        block[i] = S[i]
    return block

def KeccakSponge(bits, input, delimitedSuffix, output):
    rate = 1600 - bits
    blockSize = rate // 8
    S = [0] * 25
    inputOffset = 0
    inputByteLen = len(input)
    while (inputByteLen > rate // 8):
        for i in range(blockSize):
            S[i] ^= input[inputOffset + i]
        KeccakF1600(S)
        inputOffset += blockSize
        inputByteLen -= blockSize
    block = [0] * blockSize
    for i in range(inputByteLen):
        block[i] = input[inputOffset + i]
    block[inputByteLen] = delimitedSuffix
    block[blockSize - 1] |= 0x80
    for i in range(blockSize):
        S[i] ^= block[i]
    if (delimitedSuffix == 0x06):
        KeccakF1600(S)
    return S

if __name__ == '__main__':
    print(Keccak(256, b"abc", 0x06, 256))

    
