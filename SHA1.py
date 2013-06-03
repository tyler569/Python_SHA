import sys


def _init_vars():
    '''
    Initialises variables for the SHA1 hash algorithm
    '''
    hash_vars = [
        0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
    ]
    ROUND_CONSTS = [
        0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6
    ]
    return hash_vars, ROUND_CONSTS

def _msg2chunks(message):
    '''
    Converts message input to SHA1 chunks.
    
    Takes message as str

    Returns array of SHA1 chunks corresponding to input data and function
    as binary string
    '''
    message_bin = ''

    for i in message.encode():
        message_bin += fill_0s(bin(i)[2:], 8)
    length = len(message_bin)
    message_bin += '1' # Appended bit
    
    pad_0s = '0' * (512 - (len(message_bin) + 64) % 512)
    chunk_bin = message_bin + pad_0s
    length_bin = fill_0s(bin(length)[2:], 64)
    chunk_bin += length_bin
    chunks = []
    
    if len(chunk_bin) > 512:
        for i in range(int(len(chunk_bin) / 512)):
            chunks.append(chunk_bin[512*i:512*(i+1)])
    else:
        chunks = [chunk_bin]
    return chunks
    
def fill_0s(val, places):
    '''
    Fills in the dropped 0's for binary numbers

    Takes val as str

    Returns same number but with n 0's added such that len(input + n*'0')
    is == places.
    '''
    out = ((places - len(val)) * '0') + val
    return out

def _words(chunk_bin):
    '''
    Given an SHA1 chunk and information about what function is being called,
    function generated the word array corresponding to it

    Takes SHA1 chunk as binary string

    Returns array of (ct) binary words as strings for use in SHA1 calculation
    '''
    w = [0 for i in range(80)]
    for i in range(16):
        start = 32*i
        end = 32*(i+1)
        w[i] = int(chunk_bin[start:end], 2)
    for i in range(16, 80):
        w[i] = rol(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
    return w
    
def rol(num, val):
    '''
    Binary left rotate

    Takes number to rotate (num) as int and places to rotate (val) as int

    Returns int - rotated number
    '''
    pre = num << val
    over = pre - (pre % 2**32)
    pre -= over
    post = over >> 32
    out = pre + post
    return out
    
def sha1hash(message):
    '''
    Main loop of the SHA1 hash algorithm

    Takes data and digest bits as input

    Returns hash digest as int
    '''
    chunks = _msg2chunks(message)
    h, k = _init_vars()
    for chunk in chunks:
        xs = h[:]
        w = _words(chunk)
        for i in range(80):
            if i in range(20):
                f = (xs[1] & xs[2]) | (~xs[1] & xs[3])
            elif i in range(20, 40):
                f = xs[1] ^ xs[2] ^ xs[3]
            elif i in range(40, 60):
                f = (xs[1] & xs[2]) | (xs[1] & xs[3]) | (xs[2] & xs[3])
            elif i in range(60, 80):
                f = xs[1] ^ xs[2] ^ xs[3]
            temp = (rol(xs[0], 5) + f + xs[4] + k[i//20] + w[i]) % 2**32
            xs = [temp, xs[0], rol(xs[1], 30), xs[2], xs[3]]
            #print(str(i) + ': ' + ' '.join([hex(int(i))[2:] for i in xs])) ##
        h = [(h[i] + xs[i]) % 2**32 for i in range(5)]
    digest = sum([h[i] << 32 * (4-i) for i in range(5)])
    return(digest)

def main():
    try:
        message = sys.argv[1]
    except IndexError:
        message = ''
    digest = sha1hash(message)
    print(hex(digest))

if __name__ == '__main__':
    main()
	