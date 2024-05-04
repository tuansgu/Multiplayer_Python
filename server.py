import socket
import threading
import pygame

HOST = '192.168.1.12'
PORT = 5555
MAX_CLIENTS = 2  # Số lượng kết nối tối đa cho phép

clients = []
ready_count = 0

def handle_client(client_socket):
    global ready_count
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received:", data)
            # Xử lý dữ liệu nhận được từ client

            # Kiểm tra nếu client đã sẵn sàng
            print(data)
            if data == "tuan":
                ready_count += 1
                print(ready_count)
                if ready_count == MAX_CLIENTS:
                    # Gửi sự kiện USEREVENT cho tất cả client để thông báo đã đủ người chơi
                    print("thành công")
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()

def wait_enemy():
    global ready_count
    while ready_count < MAX_CLIENTS:
        pass
    # Khi cả hai người chơi đều sẵn sàng, tiếp tục với trò chơi
    print("Both players are ready, starting the game...")

def start_server():
    global ready_count
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CLIENTS)
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            clients.append(client_socket)

            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()

            if len(clients) == MAX_CLIENTS:
                wait_enemy()

    except Exception as e:
        print("Error:", e)
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
