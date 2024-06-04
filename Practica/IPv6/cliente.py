# Cliente

# 1) Importar el módulo socket: Permite crear y gestionar conexiones de red.
import socket

# 2) Crear un socket IPv6: socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) 
# crea un socket que utiliza IPv6 (AF_INET6) y el protocolo UDP (SOCK_DGRAM).
client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

# 3) Definir la dirección del servidor y el puerto: server_address = ('::1', 12345) 
# especifica la dirección IPv6 local ::1 y el puerto 12345 del servidor al que el cliente 
# se conectará.
server_address = ('::1', 12345)  # Usamos '::1' como la dirección IPv6 local y el puerto 12345

# 4) Mensaje a enviar: message = "Hola, servidor" define el mensaje que el cliente 
# enviará al servidor.
message = "Hola, servidor"

try:
    # 5) Enviar datos: client_socket.sendto(message.encode(), server_address) 
    # envía el mensaje codificado al servidor.
    client_socket.sendto(message.encode(), server_address)

    # 6) Recibir respuesta: data, server = client_socket.recvfrom(1024) 
    # recibe datos del servidor, con un tamaño máximo de 1024 bytes.
    data, server = client_socket.recvfrom(1024)
    # 7) Imprimir la respuesta: imprime la respuesta recibida del servidor.
    print(f"Recibido desde el servidor: {data.decode()}")
finally:
    # 8) Cerrar el socket: client_socket.close() cierra el socket del cliente.
    client_socket.close()