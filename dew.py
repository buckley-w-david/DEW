import secrets
import operator, functools

#LFSH combine function, takes current state of the register and a combination polynomial to specify which bits to extract
def deBruijn(seed, poly):
    R = combine(seed, poly)
    extra = seed == 0
    return R ^ extra

def combine(seed, poly):
    bits = [(seed >> (exponent-1)) & 1 for exponent in poly] #extract the bits for the given polynomial
    return functools.reduce(operator.xor, bits) #XOR all bits extracted from the seed together

#Alternating Step generator used to expand key to match the length of the data
def expand(key, size, nonce0, nonce1):
    mask_256 = (2**256)-1
    mask_255 = (2**255)-1
    mast_253 = (2**253)-1
    
    control = key #length 256 LFSR
    LFSR0 = nonce0 #length 253 LFSR
    LFSR1 = nonce1 #length 255 LFSR
    expanded_key = 0

    LFSR0_out = 0 
    LFSR1_out = 0 
    
    warmup = -256 #have initial warmup phase to make output rely on both nonces and key, instead of just the nonces
    for _ in range(size-warmup):
        control_out = control >> 255 #extract MSB
        next_in = deBruijn(control, (12, 48, 115, 133, 213, 256)) #1 + x^12 + x^48 + x^115 + x^133 + x^213 + x^256
        control = ((control << 1) | next_in) & mask_256 #Shift control 1 to the left, and insert the next_in to the LSB, then & with (2^256)-1 to cut off MSB (output)

        if control_out:
            LFSR0_out = LFSR0 >> 253
            next_in = combine(LFSR0, (5, 27, 82, 100, 158, 253)) #1 + x^5 + x^27 + x^82 + x^100 + x^158 + x^253
            LFSR0 = ((LFSR0 << 1) | next_in) & mast_253
        else:
            LFSR1_out = LFSR1 >> 254
            next_in = combine(LFSR1, (50, 82, 116, 153, 166, 255)) #1 + x^50 + x^82 + x^116 + x^153 + x^166 + x^255
            LFSR1 = ((LFSR1 << 1) | next_in) & mask_255

        if warmup > 0:
            expanded_key = (expanded_key << 1) | (LFSR0_out ^ LFSR1_out) #shift output stream one to the left, and insert new output into LSB
        warmup += 1
        
    return expanded_key.to_bytes(size//8, byteorder='little') #convert the expanded key to bytes to xor with the file bytes

#If transforms text from plaintext to ciphertext, or ciphertext to plaintext
def transform(stream, key, nonce1, nonce2):
    expanded_key = expand(key, len(stream)*8, nonce1, nonce2) #return a bytes object
    transformed_stream = bytearray()
    for byte_key, byte_stream in zip(expanded_key, stream):
        transformed_stream.append(byte_key ^ byte_stream)

    return bytes(transformed_stream)
