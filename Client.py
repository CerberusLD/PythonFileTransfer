import socket
import os
from tqdm import tqdm

def send_files(folder_path, server_address, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_address, server_port))

        # Enviar el nombre de la carpeta al servidor
        folder_name = os.path.basename(folder_path)
        client_socket.send(folder_name.encode())

        # Enviar archivos al servidor
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Enviar nombre del archivo
            client_socket.send(file_name.encode())

            # Enviar tamaño del archivo
            file_size = os.path.getsize(file_path)
            client_socket.send(str(file_size).encode())

            # Inicializar la barra de progreso
            progress_bar = tqdm(total=file_size, desc=f"Enviando '{file_name}'")

            # Enviar el archivo al servidor
            with open(file_path, 'rb') as file:
                while True:
                    data = file.read(BUFFER_SIZE)
                    if not data:
                        break
                    client_socket.send(data)
                    progress_bar.update(len(data))

            progress_bar.close()

        # Informar al servidor que la transferencia ha terminado
        client_socket.send(b'')

        print("\nTransferencia completada.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión del cliente
        client_socket.close()

if __name__ == "__main__":
    folder_to_send = '/'
    server_address = '127.0.0.1'
    server_port = 5555

    send_files(folder_to_send, server_address, server_port)
