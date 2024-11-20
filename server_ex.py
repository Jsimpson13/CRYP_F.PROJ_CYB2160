import socket
keytest=345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Listen on all interfaces, port 12345
server_socket.listen(1)
print("Server is listening for connections...")
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")
conn.sendall(keytest)
print("Public key sent to the client.")