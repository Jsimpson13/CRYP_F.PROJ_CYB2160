import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization

# Generate parameters for Diffie-Hellman
parameters = dh.generate_parameters(generator=2, key_size=2048)

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)

print("Server is listening for connections...")

# Accept a connection from a client
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Server generates a private key and public key
server_private_key = parameters.generate_private_key()
server_public_key = server_private_key.public_key()

# Serialize server's public key and parameters
server_parameters_bytes = parameters.parameter_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.ParameterFormat.PKCS3
)
server_public_bytes = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Send parameters and public key to the client
conn.sendall(server_parameters_bytes)
print("Public parameters sent to the client.")
conn.sendall(server_public_bytes)
print("Server's public key sent to the client.")

# Receive client's public key
client_public_bytes = conn.recv(4096)
client_public_key = serialization.load_pem_public_key(client_public_bytes)

# Compute the shared key
server_shared_key = server_private_key.exchange(client_public_key)

# Derive a symmetric key from the shared key
derived_key = HKDF(
    algorithm=SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
).derive(server_shared_key)
print(f"Derived symmetric key: {derived_key.hex()}")

try:
    while True:
        # Receive a message from the client
        client_message = conn.recv(1024).decode('utf-8')
        if client_message.lower() == "exit":
            print("Client disconnected.")
            break
        print(f"Client: {client_message}")

        # Send a message to the client
        server_message = input("Server: ")
        conn.sendall(server_message.encode('utf-8'))
        if server_message.lower() == "exit":
            print("Server disconnected.")
            break
finally:
# Close the connection and server socket
    conn.close()
    server_socket.close()