import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('SERVER_IP_ADDRESS', 12345))
keytest1=client_socket.recv(4096)
print("Recieved public key from the server. ")
