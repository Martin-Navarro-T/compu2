import cv2
import numpy as np
import mmap
import os
import multiprocessing as mp
import tempfile
import sys
import time

def cargar_imagen(file_path):
    imagen = cv2.imread(file_path)
    return imagen, imagen.shape[1], imagen.shape[0]

def dividir_imagen(imagen, num_divisiones):
    altura, ancho = imagen.shape[:2]
    altura_division = (altura + num_divisiones - 1) // num_divisiones  # Altura ajustada para dividir exactamente
    nueva_altura = altura_division * num_divisiones
    padding = nueva_altura - altura
    imagen_padded = cv2.copyMakeBorder(imagen, 0, padding, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    divisiones = [
        imagen_padded[i * altura_division:(i + 1) * altura_division, :]
        for i in range(num_divisiones)
    ]
    return divisiones

def aplicar_filtro(division):
    resultado = cv2.bitwise_not(division)
    return resultado

def procesar_imagen(imagen):
    num_divisiones = mp.cpu_count()
    procesos = []
    fifo_paths = []

    altura, ancho = imagen.shape[:2]
    altura_division = (altura + num_divisiones - 1) // num_divisiones
    imagen_size = ancho * altura_division * 3 * num_divisiones  # Tamaño total ajustado

    # Crear un archivo temporal para usar mmap
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b'\x00' * imagen_size)
    temp_file.close()

    # Mapear el archivo a memoria
    with open(temp_file.name, 'r+b') as f:
        mem_map = mmap.mmap(f.fileno(), imagen_size)

        def worker(division, fifo_path, indice, start_idx):
            imagen_procesada = aplicar_filtro(division)
            division_flat = imagen_procesada.flatten()

            # Verificar tamaño de datos
            if len(division_flat) != (division.shape[0] * division.shape[1] * 3):
                raise ValueError("Data size mismatch")

            # Escribir los datos procesados en el mmap
            mem_map.seek(start_idx)
            mem_map.write(division_flat.tobytes())
            

            # Señalar la finalización del proceso escribiendo el índice en el FIFO
            with open(fifo_path, 'w') as fifo:
                fifo.write(f'{indice}\n')

        divisiones = dividir_imagen(imagen, num_divisiones)

        # Crear FIFO para la comunicación
        for i in range(num_divisiones):
            fifo_path = f'/tmp/fifo_{i}'
            if os.path.exists(fifo_path):
                os.remove(fifo_path)
            os.mkfifo(fifo_path)
            fifo_paths.append(fifo_path)

        for i, division in enumerate(divisiones):
            fifo_path = fifo_paths[i]
            start_idx = i * division.size * division.itemsize
            print(f'Indice: {i}')
            print(f'Tamaño de la división: {division.size * division.itemsize}')
            p = mp.Process(target=worker, args=(division, fifo_path, i, start_idx))
            procesos.append(p)
            p.start()

        divisiones_procesadas = [None] * num_divisiones
        for i in range(num_divisiones):
            fifo_path = fifo_paths[i]
            with open(fifo_path, 'r') as fifo:
                indice = int(fifo.readline().strip())
            start_idx = indice * divisiones[indice].size * divisiones[indice].itemsize
            mem_map.seek(start_idx)
            division_flat = mem_map.read(divisiones[indice].size * divisiones[indice].itemsize)
            divisiones_procesadas[indice] = np.frombuffer(division_flat, dtype=np.uint8).reshape(divisiones[indice].shape)

        for p in procesos:
            p.join()

    # Eliminar el archivo temporal y FIFOs
    os.remove(temp_file.name)
    for fifo_path in fifo_paths:
        os.remove(fifo_path)

    return divisiones_procesadas, ancho

def unir_imagenes(divisiones_procesadas, ancho, ruta_guardado):
    altura_total = sum(division.shape[0] for division in divisiones_procesadas)
    nueva_imagen = np.zeros((altura_total, ancho, 3), dtype=np.uint8)
    y_offset = 0
    for division in divisiones_procesadas:
        nueva_imagen[y_offset:y_offset + division.shape[0], :] = division
        y_offset += division.shape[0]
    cv2.imwrite(ruta_guardado, nueva_imagen)

def limpiar(signum, frame, procesos):
    print("Interrupción recibida, limpiando...")
    for p in procesos:
        if p.is_alive():
            p.terminate()
    sys.exit(0)