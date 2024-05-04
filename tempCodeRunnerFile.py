import socket
import threading

HOST = '192.168.1.12'
PORT = 5555
MAX_CLIENTS = 2  # Số lượng kết nối tối đa cho phép

clients = []

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received:", data)
            # Xử lý dữ liệu nhận được từ client
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CLIENTS)
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

            clients.append(client_socket)  # Thêm client vào danh sách

    except Exception as e:
        print("Error:", e)
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
