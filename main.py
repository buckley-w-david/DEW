#!/usr/bin/python3

import argparse
from secrets import randbits
import dew

def _encrypt(args):
    key = randbits(256)
    nonce1 = randbits(256)
    nonce2 = randbits(256)
    
    if (args.cmdtext):
        with open(args.outfile, 'wb') as out:
            result = dew.transform(args.infile.encode(), key, nonce1, nonce2)
            out.write(nonce1.to_bytes(32, byteorder='little')
                      + nonce2.to_bytes(32, byteorder='little')
                      + result)
    else:    
        with open('{}'.format(args.infile), 'rb') as f, open(args.outfile, 'wb') as out:
            result = dew.transform(f.read(), key, nonce1, nonce2)
            out.write(nonce1.to_bytes(32, byteorder='little')
                      + nonce2.to_bytes(32, byteorder='little')
                      + result)
            
    with open('{}.key'.format(args.outfile), 'wb') as out:
        out.write(key.to_bytes(32, byteorder='little'))

def _decrypt(args):
    with open(args.keyfile, 'rb') as f:
        key = int.from_bytes(f.read(), byteorder='little')
        
    with open('{}'.format(args.infile), 'rb') as f, open(args.outfile, 'wb') as out:
        nonce1 = int.from_bytes(f.read(32), byteorder='little')
        nonce2 = int.from_bytes(f.read(32), byteorder='little')
        
        result = dew.transform(f.read(), key, nonce1, nonce2)
        out.write(result)
            

if __name__ == '__main__':
    #Main argument parser
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='operation')
    subparsers.required = True
    
    #Subparser for encryption
    parser_e = subparsers.add_parser('encrypt', help='Option to select to encrypt input')
    parser_e.add_argument('--cmdtext', action='store_true',
                        help="Specifiy this command to treat the 'infile' argument as the text the encrypt")
    parser_e.add_argument('infile', help="The plaintext wanted to be encrypted/decrypted")
    parser_e.add_argument('outfile', help="Name of output encrypted file")
    parser_e.set_defaults(func=_encrypt)

    #Subparer for decryption
    parser_d = subparsers.add_parser('decrypt', help='Option to select to decrypt input')
    parser_d.add_argument('infile', help="The plaintext wanted to be encrypted/decrypted")
    parser_d.add_argument('keyfile', help="The file generated holding the key during encryption")
    parser_d.add_argument('outfile', help="Name of output unencrypted file")
    parser_d.set_defaults(func=_decrypt)

    args = parser.parse_args()
    args.func(args)
