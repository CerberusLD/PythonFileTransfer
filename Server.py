import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 5555
BUFFER_SIZE = 1024
UPLOADS_DIR = 'uploads'

os.makedirs(UPLOADS_DIR, exist_ok=True)

def handle_client(client_socket):
    try:
        # Recibir el nombre de la carpeta
        folder_name = client_socket.recv(BUFFER_SIZE).decode()

        # Crear la carpeta en el servidor
        folder_path = os.path.join(UPLOADS_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Recibir y guardar archivos
        while True:
            file_name = client_socket.recv(BUFFER_SIZE).decode()
            if not file_name:
                break

            file_path = os.path.join(folder_path, file_name)

            # Recibir tamaño del archivo
            file_size = int(client_socket.recv(BUFFER_SIZE).decode())

            # Inicializar la barra de progreso
            progress = 0
            print(f"Recibiendo '{file_name}'...")

            # Recibir y guardar el archivo
            with open(file_path, 'wb') as file:
                while progress < file_size:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data:
                        break
                    file.write(data)
                    progress += len(data)
                    print(f"Progreso: {progress}/{file_size}", end='\r')

            print(f"\nArchivo '{file_name}' recibido y guardado en '{file_path}'")

        print("Transferencia completada.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión del cliente
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión aceptada desde {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
