import socket

HOST = (socket.gethostname(), 20_000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# от созданного клиентского сокета коннектимся к созданному серверу
client.connect(HOST)

# метод recv поможет нам получить какие-то данные от сервера
# 1024 это размер временного буфера для хранения двоичного значения (данных от сервера) в количестве байт
msg = client.recv(1024)
print(msg.decode('utf-8'))
