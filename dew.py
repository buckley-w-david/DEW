import secrets
import operator, functools

#linear control LFSH combine
def combine(seed, poly):
    bits = [(seed >> (exponent-1)) & 1 for exponent in poly]
    return functools.reduce(operator.xor, bits)

def expand(key, size):
    mask = 115792089237316195423570985008687907853269984665640564039457584007913129639935 #(2^256)-1
    control = key
    LFSR0 = key-5 & mask #Temporary
    LFSR1 = key+5 & mask #Temporary
    expanded_key = 0

    LFSR0_out = 0
    LFSR1_out = 0
    for _ in range(size):
        control_out = control >> 255 #extract MSB
        next_in = combine(control, (12, 48, 115, 133, 213, 256)) #1 + x^12 + x^48 + x^115 + x^133 + x^213 + x^256
        control = ((control << 1) | next_in) & mask #Shift control 1 to the left, and insert the next_in to the LSB, then & with (2^256)-1 to cut off MSB (output)

        if control_out:
            LFSR0_out = LFSR0 >> 255
            next_in = combine(LFSR0, (12, 48, 115, 133, 213, 256)) #temporary
            LFSR0 = ((LFSR0 << 1) | next_in) & mask
        else:
            LFSR1_out = LFSR1 >> 255
            next_in = combine(LFSR1, (12, 48, 115, 133, 213, 256)) #temporary
            LFSR1 = ((LFSR1 << 1) | next_in) & mask
            
        expanded_key = (expanded_key << 1) | (LFSR0_out ^ LFSR1_out) #shift output stream one to the left, and insert new output into LSB
        
    return expanded_key.to_bytes(size//8, byteorder='little')

def transform(stream, key):
    expanded_key = expand(key, len(stream)*8) #return a bytes object
    transformed_stream = bytes()
    for byte_key, byte_stream in zip(expanded_key, stream):
        transformed_stream += (byte_key ^ byte_stream).to_bytes(1, byteorder='little')

    return transformed_stream
