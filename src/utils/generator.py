"""
This generate ANYTHING,
even rsa key...
"""
from Crypto.PublicKey import RSA

def generate_RSA(bits=2048):
    '''
    Stolen from https://gist.github.com/lkdocs/6519378
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key
