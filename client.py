import socket
import sys


'''
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send HTTP request
    request = b'GET /index.html HTTP/1.1\nHost: localhost:8080\n\n'
    print('Sending {!r}'.format(request))
    sock.sendall(request)

    # Receive the response
    response = sock.recv(1024)
    print('Received:\n', response.decode())

finally:
    print('Closing socket')
    sock.close()
'''

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8080)
print('Connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send HTTP request
    request = b'GET /index.html HTTP/1.1\nHost: localhost:8080\n\n'
    print('Sending {!r}'.format(request))
    sock.sendall(request)

    # Receive the response
    response = sock.recv(1024)
    with open('index.html', 'wb') as f:
        while response:
            f.write(response)
            response = sock.recv(1024)

    # Send another HTTP request
    request = b'GET /indoSbgPenghasiKopi.png HTTP/1.1\nHost: localhost:8080\n\n'
    print('Sending {!r}'.format(request))
    sock.sendall(request)

    # Receive the response
    response = sock.recv(1024)
    with open('indoSbgPenghasiKopi.png', 'wb') as f:
        while response:
            f.write(response)
            response = sock.recv(1024)

finally:
    print('Closing socket')
    sock.close()