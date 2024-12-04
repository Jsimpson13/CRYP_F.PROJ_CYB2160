import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

from Decrypt import DECS
from Encoding import Encoding

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('127.0.0.1', 12345))
print("Connected to the server.")

# Receive Diffie-Hellman parameters from the server
parameters_bytes = client_socket.recv(4096)
parameters = serialization.load_pem_parameters(parameters_bytes)

# Receive the server's public key
server_public_bytes = client_socket.recv(4096)
server_public_key = serialization.load_pem_public_key(server_public_bytes)

# Client generates a private key and public key
client_private_key = parameters.generate_private_key()
client_public_key = client_private_key.public_key()

# Serialize the client's public key and send it to the server
client_public_bytes = client_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
client_socket.sendall(client_public_bytes)
print("Client's public key sent to the server.")

# Compute the shared key
client_shared_key = client_private_key.exchange(server_public_key)

# Derive a symmetric key from the shared key
derived_key = HKDF(
    algorithm=SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(client_shared_key)
numeric_key = int.from_bytes(derived_key[:4], 'big')  # Derive numeric key
print(f"Derived symmetric key: {derived_key.hex()}")
print(f"Numeric key: {numeric_key}")

try:
    while True:
        # Send a message to the server
        raw_message = input("Client: ")
        if raw_message.lower() == "exit":
            print("Client disconnected.")
            client_socket.sendall(b"exit")
            break

        client_message = Encrypt(raw_message, numeric_key)
        client_socket.sendall(client_message.encode('utf-8'))

        # Receive a message from the server
        server_message = client_socket.recv(1024).decode('utf-8')
        if server_message.lower() == "exit":
            print("Server disconnected.")
            break

        print(f"Server: {Decrypt.DECS(server_message, numeric_key)}")
finally:
    client_socket.close()