import secrets

def expand(key, size):
    return key.to_bytes(32, byteorder='little').rjust(size, (5).to_bytes(1, byteorder='little'))

def transform(stream, key):
    expanded_key = expand(key, len(stream)) #return a bytes object
    transformed_stream = bytes()
    for byte_key, byte_stream in zip(expanded_key, stream):
        transformed_stream += (byte_key ^ byte_stream).to_bytes(1, byteorder='little')

    return transformed_stream
