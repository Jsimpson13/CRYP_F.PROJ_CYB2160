import socket

# Public key to send
keytest = "345"

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to localhost and port 12345
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)

print("Server is listening for connections...")

# Accept a connection from a client
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Send the public key to the client
conn.sendall(keytest.encode('utf-8'))
print("Public key sent to the client.")

# Close the connection and server socket
conn.close()
server_socket.close()
