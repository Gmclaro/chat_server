import socket
import threading

def handle_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received message from client {client_id}: {message}")
            broadcast(f"Client {client_id}: {message}")
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def broadcast(message):
    for client_id, client_socket in enumerate(clients):
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error broadcasting message: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('10.112.40.222', 5555))
    server.listen(5)
    print("Server listening on port 5555")

    client_id = 0
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_handler.start()
        client_id += 1

clients = []

if __name__ == "__main__":
    start_server()
