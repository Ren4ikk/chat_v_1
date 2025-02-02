# Исправленный код сервера
import socket
import threading

# Задаем ip и порт хоста
HOST = ('0.0.0.0', 20000)

# Создание сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(HOST)
server_socket.listen()

print('Сервер запущен и прослушивает порт 20000')

clients = []  # Список подключенных клиентов


def broadcast(message, sender_socket):
    """Рассылка сообщения всем клиентам, кроме отправителя."""
    message += b'\n'  # Добавляем разделитель новой строки для корректного разделения сообщений на стороне клиента
    for client in clients:
        if client != sender_socket:  # Проверяем, что это не тот клиент, который отправил сообщение
            try:
                client.sendall(message)  # Отправляем сообщение клиенту
            except:
                client.close()  # В случае ошибки закрываем соединение
                clients.remove(client)  # Удаляем клиента из списка подключённых


def handle_client(client_socket, addr):
    """Обработка каждого клиента в отдельном потоке."""
    print(f"Подключен клиент {addr}")
    clients.append(client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Сообщение от {addr}: {message.decode().strip()}")
            broadcast(message, client_socket)
    except (ConnectionResetError, BrokenPipeError):
        print(f"Соединение с {addr} потеряно.")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Клиент {addr} отключен.")


while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
