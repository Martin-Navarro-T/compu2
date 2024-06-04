#Servidor

#1) Importar el módulo socket: Permite crear y gestionar conexiones de red.
import socket

# 2) Crear un socket IPv6: socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
# crea un socket que utiliza IPv6 (AF_INET6) y el protocolo TCP (SOCK_STREAM).
server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# 3) Asociar el socket a una dirección y puerto: server_socket.bind(server_address) 
# asocia el socket a la dirección IPv6 local ::1 (equivalente a localhost en IPv6) 
# y al puerto 12345.
server_address = ('::1', 12345)  # Usamos '::1' como la dirección IPv6 local y el puerto 12345
server_socket.bind(server_address)

# 4) Escuchar conexiones entrantes: server_socket.listen(5) permite al servidor aceptar 
# conexiones entrantes. El argumento 5 especifica el número máximo de conexiones en espera.
server_socket.listen(5)  # El argumento 1 indica el número máximo de conexiones en espera

print("Servidor esperando conexiones...")

# 5) Esperar y aceptar conexiones: El servidor entra en un bucle infinito con while True: 
# para aceptar conexiones. server_socket.accept() espera una conexión entrante y devuelve 
# un nuevo socket para comunicarse con el cliente y la dirección del cliente.
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Conexión aceptada desde {client_address}")

    # Manejar la comunicación con el cliente aquí

