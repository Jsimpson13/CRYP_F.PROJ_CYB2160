import cryptography
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

# Generate parameters (shared between client and server)
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Server generates a private key and public key
server_private_key = parameters.generate_private_key()
server_public_key = server_private_key.public_key()

# Client generates a private key and public key
client_private_key = parameters.generate_private_key()
client_public_key = client_private_key.public_key()

# Exchange public keys
server_public_bytes = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

client_public_bytes = client_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Deserialize the public keys
server_public_key = serialization.load_pem_public_key(server_public_bytes)
client_public_key = serialization.load_pem_public_key(client_public_bytes)

# Compute shared keys
server_shared_key = server_private_key.exchange(client_public_key)
client_shared_key = client_private_key.exchange(server_public_key)

# Derive a symmetric key from the shared secret
derived_key = HKDF(
    algorithm=SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(server_shared_key)

# Verify that both parties derived the same key
assert server_shared_key == client_shared_key
print("Shared key established successfully!")
print(f"Derived symmetric key: {derived_key.hex()}")
