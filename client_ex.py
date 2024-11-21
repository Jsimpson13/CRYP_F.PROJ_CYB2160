import socket

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(('127.0.0.1', 12345))

# Receive the public key from the server
keytest1 = client_socket.recv(4096)
print("Received public key from the server:", keytest1.decode('utf-8'))

# Close the client socket
client_socket.close()
