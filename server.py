import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 8080)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
print('Waiting for a connection...')

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        print('Connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            # Receive the data
            data = connection.recv(1024).decode()

            if data:
                # Parse the request
                request_method = data.split(' ')[0]
                request_file = data.split(' ')[1]
                
                # Check if file exists
                if os.path.isfile(request_file[1:]):
                    # Send HTTP response
                    if request_file.endswith('.html'):
                        content_type = 'text/html'
                    elif request_file.endswith('.jpg'):
                        content_type = 'image/jpeg'
                    else:
                        content_type = 'text/plain'
                    
                    response_header = 'HTTP/1.1 200 OK\nContent-Type: {}\n\n'.format(content_type)
                    with open(request_file[1:], 'rb') as f:
                        response_data = f.read()
                    
                else:
                    # Send 404 Not Found response
                    response_header = 'HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n'
                    response_data = b'<html><body><h1>404 Not Found</h1></body></html>'
                    
                response = response_header.encode() + response_data
                connection.sendall(response)
                
            else:
                print('No data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
