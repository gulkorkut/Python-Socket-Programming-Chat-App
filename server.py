import socket
import threading

HOST_IP = '127.0.0.1'  # Server 127.0.0.1IP address
PORT = 5000  # Server port
connected_clients = []  # Array to store connected clients

# Function to handle client connections
def handle_client(client_socket, client_address):
    print("New client connected:", client_address)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print("Received message from", client_address, ":", message)
                send_message_to_clients(message, client_address)
            else:
                delete_client(client_socket)
                print("Client disconnected:", client_address)
                break
        except:
            print("An error occurred from", client_address)
            delete_client(client_socket)
            break


# sent to all connected clients
def send_message_to_clients(message, sender_address):
    for client in connected_clients:
        if client[1] != sender_address:
            client[0].send(message.encode('utf-8'))


def delete_client(client_socket, client_address):
    for client in connected_clients:
        if client[0] == client_socket and client[1] == client_address:
            connected_clients.remove(client)
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, PORT))
    server_socket.listen(5)
    print("Server socket started on {} : {}".format(HOST_IP, PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        connected_clients.append((client_socket, client_address))
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

# Start the server
start_server()
