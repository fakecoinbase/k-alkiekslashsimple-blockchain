import pickle

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


pairs = []
for i in range(50):
    a = rsa.generate_private_key(public_exponent=65537,key_size=1028,backend=default_backend())
    s_pem = a.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.BestAvailableEncryption(b'password'))
    p_pem = a.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    pairs.append({'sk': s_pem, 'pk': p_pem})

pickle.dump(pairs, open( "key_pairs", "wb" ))

read_pairs = pickle.load(open( "key_pairs", "rb" ))
skb = read_pairs[0]['sk']
pkb = read_pairs[0]['pk']


sk = serialization.load_pem_private_key(skb, password=b'password', backend=default_backend())
pk = serialization.load_pem_public_key(pkb, backend=default_backend())
print(sk)
print(pk)