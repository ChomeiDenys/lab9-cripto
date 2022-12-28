import hashlib
import math


def reshuffle(bit_string_32):
    if len(bit_string_32) != 32:
        raise ValueError("Вам потрібна довжина 32")
    new_string = ""
    for i in [3, 2, 1, 0]:
        new_string += bit_string_32[8 * i:8 * i + 8]
    return new_string


def reformat_hex(i):
    hex_rep = format(i, '08x')
    new_string_2 = ""
    for i in [3, 2, 1, 0]:
        new_string_2 += hex_rep[2 * i:2 * i + 2]
    return new_string_2


def pad(bit_string):
    start_length = len(bit_string)
    bit_string += '1'
    while len(bit_string) % 512 != 448:
        bit_string += '0'
    last_part = format(start_length, '064b')
    bit_string += reshuffle(last_part[32:]) + reshuffle(last_part[:32])
    return bit_string


def get_block(bit_string):
    curr_pos = 0
    while curr_pos < len(bit_string):
        curr_part = bit_string[curr_pos:curr_pos + 512]
        my_splits = []
        for i in range(16):
            my_splits.append(int(reshuffle(curr_part[32 * i:32 * i + 32]), 2))
        yield my_splits
        curr_pos += 512


def not32(i):
    i_str = format(i, '032b')
    new_str = ''
    for c in i_str:
        new_str += '1' if c == '0' else '0'
    return int(new_str, 2)


def sum32(a, b):
    return (a + b) % 2 ** 32


def left_rot_32(i, s):
    return (i << s) ^ (i >> (32 - s))


def md5me(test_string):
    bs = ''
    for i in test_string:
        bs += format(ord(i), '08b')
    bs = pad(bs)

    t_vals = [int(2 ** 32 * abs(math.sin(i + 1))) for i in range(64)]

    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, \
         5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, \
         4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, \
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    for m in get_block(bs):
        A = a0
        B = b0
        C = c0
        D = d0
        for i in range(64):
            if i <= 15:
                # f = (B & C) | (not32(B) & D)
                f = D ^ (B & (C ^ D))
                g = i
            elif i <= 31:
                # f = (D & B) | (not32(D) & C)
                f = C ^ (D & (B ^ C))
                g = (5 * i + 1) % 16
            elif i <= 47:
                f = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                f = C ^ (B | not32(D))
                g = (7 * i) % 16
            d_temp = D
            D = C
            C = B
            B = sum32(B, left_rot_32((A + f + t_vals[i] + m[g]) % 2 ** 32, s[i]))
            A = d_temp
        a0 = sum32(a0, A)
        b0 = sum32(b0, B)
        c0 = sum32(c0, C)
        d0 = sum32(d0, D)

    digest = reformat_hex(a0) + reformat_hex(b0) + reformat_hex(c0) + reformat_hex(d0)
    return digest


if __name__ == "__main__":
    message = input('Введіть рядок для хешування за допомогою самописного md5: ')
    hash_md5 = md5me(message)
    print('"%s" = %s' % (message, hash_md5))

    message_2 = input('Введіть рядок для перевірки хешування за допомогою готового md5: ')
    hash_object = hashlib.md5(message_2.encode())
    print('"%s" = %s' % (message_2, hash_object.hexdigest()))


