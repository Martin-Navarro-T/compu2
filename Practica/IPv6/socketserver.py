import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Imprime la dirección del cliente cuando se establece una conexión
        print(f"Conexión recibida de {self.client_address}")

        # Recibe datos del cliente
        data = self.request.recv(1024).strip()
        print(f"Recibido: {data.decode()}")

        # Envia una respuesta al cliente
        response = "Mensaje recibido por el servidor"
        self.request.sendall(response.encode())

if __name__ == "__main__":
    # Crea el servidor con soporte para IPv6
    server = socketserver.ThreadingTCPServer(('::1', 12345), MyHandler)

    print("Servidor esperando conexiones...")

    # Permite que el servidor maneje múltiples conexiones en hilos separados
    server.serve_forever()