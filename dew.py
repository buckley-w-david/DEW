import secrets
import operator, functools

#Non-linear combining function
def combine(seed):
    '''1 + x^12 + x^48 + x^115 + x^133 + x^213 + x^256'''
    exponents = (12, 48, 115, 133, 213, 256)
    bits = [(seed >> (exponent-1)) & 1 for exponent in exponents]
    return functools.reduce(operator.xor, bits)

def expand(key, size):
    seed = key
    expanded_key = 0
    for _ in range(size):
        output = seed >> 255 #extract most significant
        next_in = combine(seed) #combine bits to input into linear feedback shift register (seed)
        seed = ((seed << 1) | next_in) & 115792089237316195423570985008687907853269984665640564039457584007913129639935 #Shift seed 1 to the left, and insert the next_in to the LSB, then & with (2^256)-1 to cut off MSB (output)
        expanded_key = (expanded_key << 1) | output #shift output stream one to the left, and insert new output into LSB
    return expanded_key.to_bytes(size//8, byteorder='little')

def transform(stream, key):
    expanded_key = expand(key, len(stream)*8) #return a bytes object
    transformed_stream = bytes()
    for byte_key, byte_stream in zip(expanded_key, stream):
        transformed_stream += (byte_key ^ byte_stream).to_bytes(1, byteorder='little')

    return transformed_stream
