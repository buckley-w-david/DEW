#!/usr/bin/python3

import argparse
from secrets import randbits
from io import BytesIO
import dew

def _transform(args, key):
    if (args.cmdtext):
        with BytesIO() as f, open(args.outfile, 'wb') as out:
            f.write(args.text.encode())
            f.seek(0)
            result = dew.transform(f.read(), key)
            out.write(result)
    else:    
        with open('{}'.format(args.infile), 'rb') as f, open(args.outfile, 'wb') as out:
            result = dew.transform(f.read(), key)
            out.write(result)

def _encrypt(args):
    key = randbits(256)
    _transform(argsm key)
    with open('{}.key'.format(args.outfile), 'wb') as out:
        out.write(key.to_bytes(32, byteorder='little'))

def _decrypt(args):
    with open(args.keyfile, 'rb') as f:
        key = int.from_bytes(f.read(), byteorder='little')
        
    _transform(args, key)
            

if __name__ == '__main__':
    #Main argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--cmdtext', action='store_true',
                        help="Specifiy this command to treat the 'infile' argument as the text the encrypt")

    subparsers = parser.add_subparsers(dest='operation')
    subparsers.required = True
    
    #Subparser for encryption
    parser_e = subparsers.add_parser('encrypt', help='Option to select to encrypt input')
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
