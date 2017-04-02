# Final project for cis4110

Symmetric stream cipher designed and implemented by us, implimenting key expansion using an alternating step generator with 3
linear feedback shift generators seeded with a key and 2 (single file use) nonces.

## Execution
### Encryption
usage: `main.py encrypt [-h] [--cmdtext] [--keyfile KEYFILE] infile outfile`

positional arguments:<br />
  `infile`             The plaintext wanted to be encrypted/decrypted<br />
  `outfile`            Name of output encrypted file

optional arguments:<br />
  `-h`, `--help`         show this help message and exit<br />
  `--cmdtext`          Specifiy this command to treat the 'infile' argument as
                     the text the encrypt<br />
  `--keyfile KEYFILE`  Optional keyfile to encrypt the file, truncated/padded to
                     256 bits<br />
  
Examples:
Outputs encrypted version of 'testfile.txt' into file 'encrypted_file', as well as outputs 256 bit key into 'encrypted_file.key'<br />
`>python main.py encrypt testfile.txt encrypted_file`

Outputs encrypted version of 'newfile.txt' into file 'new_encrypted' using previously generated key 'encrypted_file.key'<br />
`>python main.py encrypt --keyfile encrypted_file.key newfile.txt new_encrypted`

Outputs encrypted version of text 'This is a test' into file 'new_encrypted' using previously generated key 'encrypted_file.key'<br />
`>python main.py encrypt --cmdtext --keyfile encrypted_file.key "This is a test" new_encrypted`

### Decryption
usage: `main.py decrypt [-h] infile keyfile outfile`

positional arguments:<br />
  `infile`      The plaintext wanted to be encrypted/decrypted<br />
  `keyfile`     The file generated holding the key during encryption<br />
  `outfile`     Name of output unencrypted file

optional arguments:<br />
  `-h`, `--help`  show this help message and exit
  
Examples:
Outputs decrpyed version of 'encrypted_file' into file 'newfile.txt' using key in 'encrypted_file.key'<br />
`>python main.py decrypt encrypted_file encrypted_file.key testfile.txt`

Outputs encrypted version of 'newfile.txt' into file 'new_encrypted' using previously generated key 'encrypted_file.key'<br />
`>python main.py encrypt --keyfile encrypted_file.key newfile.txt new_encrypted`
