import socket
import os

# Define host and port
HOST = 'localhost'
PORT = 8080

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f"Server is running on {HOST}:{PORT}...")

# Define a function to handle incoming requests
def handle_request(conn, addr):
    print(f"Connection established from {addr}")
    
    # Receive data from the client
    request_data = conn.recv(1024)
    request_lines = request_data.split(b"\r\n")
    
    # Get the request method and file path
    request_parts = request_lines[0].split(b" ")
    request_method = request_parts[0].decode("utf-8")
    file_path = request_parts[1].decode("utf-8")
    
    # Set the default file to index.html
    if file_path == "/":
        file_path = "/index.html"
    
    # Check if file exists
    file_path = f".{file_path}"
    if os.path.isfile(file_path):
        # Get the file extension
        _, file_extension = os.path.splitext(file_path)
        
        # Set the content type based on the file extension
        if file_extension == ".html":
            content_type = "text/html"
        elif file_extension == ".css":
            content_type = "text/css"
        elif file_extension == ".js":
            content_type = "application/javascript"
        elif file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
            content_type = f"image/{file_extension[1:]}"
        else:
            content_type = "application/octet-stream"
        
        # Read the file content
        with open(file_path, "rb") as f:
            file_content = f.read()
            
        # Build the response header
        response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(file_content)}\r\n\r\n"
        response_header = response_header.encode("utf-8")
        
        # Send the response header and content to the client
        conn.sendall(response_header)
        conn.sendall(file_content)
    else:
        # Build the 404 response
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
        response_header = response_header.encode("utf-8")
        
        # Send the 404 response to the client
        conn.sendall(response_header)
    
    # Close the connection
    conn.close()
    print(f"Connection from {addr} closed")

# Wait for incoming connections
while True:
    conn, addr = server_socket.accept()
    handle_request(conn, addr)
