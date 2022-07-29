import random
import time
from collections import Counter

MAX = 2 ** 32
vi = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e
t = [0x79cc4519, 0x7a879d8a]

#SM3 实现
def Int2Bin(a, k):
    res = list(bin(a)[2:])
    for i in range(k - len(res)):
        res.insert(0, '0')
    return ''.join(res)


def LoopLeftShift(a, k):
    res = list(Int2Bin(a, 32))
    for i in range(k):
        temp = res.pop(0)
        res.append(temp)
    return int(''.join(res), 2)

def fillFunction(message):
    message = bin(message)[2:]
    for i in range(4):
        if (len(message) % 4 == 0):
            break
        else:
            message = '0' + message
    length = len(message)
    k = 448 - (length + 1) % 512
    if (k < 0): 
        k += 512
    addMessage = '1' + '0' * k + Int2Bin(length, 64)
    message += addMessage
    return message

def IterFunction(message):
    n = int(len(message) / 512)
    v = []
    v.append(Int2Bin(vi, 256))
    for i in range(n):
        w, w1 = msgExten(message[512 * i:512 * (i + 1)])
        temp = CF(v[i], message[512 * i:512 * (i + 1)], w, w1)
        temp = Int2Bin(temp, 256)
        v.append(temp)
    return v[n]


def msgExten(b):
    w = []
    w1 = []
    for i in range(16):
        temp = b[i * 32:(i + 1) * 32]
        w.append(int(temp, 2))
    for j in range(16, 68, 1):
        factor1 = LoopLeftShift(w[j - 3], 15)
        factor2 = LoopLeftShift(w[j - 13], 7)
        factor3 = P1(w[j - 16] ^ w[j - 9] ^ factor1)
        factor4 = factor3 ^ factor2 ^ w[j - 6]
        w.append(factor4)
    for j in range(64):
        factor1 = w[j] ^ w[j + 4]
        w1.append(factor1)
    return w, w1


def P0(X):
    return X ^ LoopLeftShift(X, 9) ^ LoopLeftShift(X, 17)

def P1(X):
    return X ^ LoopLeftShift(X, 15) ^ LoopLeftShift(X, 23)

def T(j):
    if j <= 15:
        return t[0]
    else:
        return t[1]

def FF(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (X & Z) | (Y & Z)

def GG(X, Y, Z, j):
    if j <= 15:
        return X ^ Y ^ Z
    else:
        return (X & Y) | (un(X) & Z)

def un(a):
    a = Int2Bin(a, 32)
    b = ''
    for i in a:
        if i == '0':
            b += '1'
        else:
            b += '0'
    return int(b, 2)

def CF(vi, bi, w, w1):
    A = []
    for i in range(8):
        temp = vi[32 * i:32 * (i + 1)]
        A.append(int(temp, 2))
    for j in range(64):
        factor1 = LoopLeftShift(A[0], 12)
        factor2 = LoopLeftShift(T(j), j % 32)
        SS1 = LoopLeftShift((factor1 + A[4] + factor2) % MAX, 7)
        factor3 = LoopLeftShift(A[0], 12)
        SS2 = SS1 ^ factor3
        TT1 = (FF(A[0], A[1], A[2], j) + A[3] + SS2 + w1[j]) % MAX
        TT2 = (GG(A[4], A[5], A[6], j) + A[7] + SS1 + w[j]) % MAX
        A[3] = A[2]
        A[2] = LoopLeftShift(A[1], 9)
        A[1] = A[0]
        A[0] = TT1
        A[7] = A[6]
        A[6] = LoopLeftShift(A[5], 19)
        A[5] = A[4]
        A[4] = P0(TT2)
    temp = Int2Bin(A[0], 32) + Int2Bin(A[1], 32) + Int2Bin(A[2], 32) + \
           Int2Bin(A[3], 32) + Int2Bin(A[4], 32) + Int2Bin(A[5], 32) + \
           Int2Bin(A[6], 32) + Int2Bin(A[7], 32)
    temp = int(temp, 2)
    return temp ^ int(vi, 2)

#SM3函数，输出为十六进制
def sm3(msg):
    msg = fillFunction(msg)
    hex(int(msg,2))
    res = IterFunction(msg)
    res = hex(int(res,2))
    return res[2:]

#SM3 Rho攻击
#通过构造环形结构来尝试实现碰撞，挑选构造函数为x**2+1
def rho_attack(n):
    x = random.randint(0,2**64)
    cmplist = []
    cmplist.append(sm3(x)[:n//4])
    while 1:
        x = (x**2 + 1) % (2**64)
        k = sm3(x)[:n//4]
        if k in cmplist:
            print("成功找到一个碰撞!(前{}bit)".format(n))
            break
        else:
            cmplist.append(k)

if __name__ == '__main__':
    start = time.time()
    rho_attack(8)
    end = time.time()
    print('共耗时',end - start,'秒')