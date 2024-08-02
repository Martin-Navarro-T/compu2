import multiprocessing as mp
import cv2
import numpy as np
import sys

def cargar_imagen(file_path):
    imagen = cv2.imread(file_path)
    return imagen, imagen.shape[1], imagen.shape[0]

def dividir_imagen(imagen, num_divisiones):
    altura, ancho = imagen.shape[:2]
    altura_division = altura // num_divisiones
    divisiones = [
        imagen[i * altura_division:(i + 1) * altura_division, :]
        for i in range(num_divisiones)
    ]
    return divisiones

def aplicar_filtro(division):
    resultado = cv2.bitwise_not(division)
    return resultado

def procesar_imagen(imagen):
    num_divisiones = mp.cpu_count()
    procesos = []
    parent_pipes = []
    shared_array = mp.Array('B', imagen.size) 

    def worker(division, conn, indice, shared_array, start_idx, size):
        imagen_procesada = aplicar_filtro(division)
        conn.send(indice)
        conn.close()
        division_flat = imagen_procesada.flatten().tolist()
        shared_array[start_idx:start_idx + size] = division_flat

    divisiones = dividir_imagen(imagen, num_divisiones)
    altura_division = imagen.shape[0] // num_divisiones

    for i, division in enumerate(divisiones):
        parent_conn, child_conn = mp.Pipe()
        parent_pipes.append(parent_conn)
        start_idx = i * division.size
        p = mp.Process(target=worker, args=(division, child_conn, i, shared_array, start_idx, division.size))
        procesos.append(p)
        p.start()

    divisiones_procesadas = [None] * num_divisiones
    for i in range(num_divisiones):
        indice = parent_pipes[i].recv()
        parent_pipes[i].close()
        start_idx = indice * divisiones[indice].size
        division_flat = bytes(shared_array[start_idx:start_idx + divisiones[indice].size])
        divisiones_procesadas[indice] = np.frombuffer(division_flat, dtype=np.uint8).reshape(divisiones[indice].shape)

    for p in procesos:
        p.join()

    return divisiones_procesadas, imagen.shape[1]

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
