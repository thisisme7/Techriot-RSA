import rsa
from base64 import b64encode, b64decode

def keygen(keysize): # key size = 512, 1024, 2048, 4096
    
    # Generate the key pair
    pubkey, privkey = rsa.newkeys(keysize)

    # Save the private key to a file
    with open('keypair/private.pem', mode='wb') as prvKeyFile:
        prvKeyFile.write(privkey.save_pkcs1())

    # Save the public key to a file
    with open('keypair/public.pem', mode='wb') as pubKeyFile:
        pubKeyFile.write(pubkey.save_pkcs1())


def encrypt(pubkey, plaintext):
    try:
        pubkey = rsa.PublicKey.load_pkcs1(pubkey)
        scrambled = rsa.encrypt(plaintext.encode('ascii'), pubkey)
        return b64encode(scrambled).decode("ascii")
    except:
        return "ERROR: Invalid key!"

def decrypt(prvkey, b64text):
    try:
        prvkey = rsa.PrivateKey.load_pkcs1(prvkey)
        plaintext = rsa.decrypt(b64decode(b64text.encode('ascii')), prvkey)
        return plaintext.decode()
    except:
        return "ERROR: Invalid private key or ciphertext!"
    
