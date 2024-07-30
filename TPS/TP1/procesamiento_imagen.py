import multiprocessing as mp
import cv2
import numpy as np
import sys

def cargar_imagen(file_path):
    #Carga una imagen desde el disco usando un archivo especificado.
    imagen = cv2.imread(file_path)
    return imagen, imagen.shape[1], imagen.shape[0]

def dividir_imagen(imagen, num_divisiones):
    #Divide la imagen en partes iguales para ser procesadas en paralelo.
    altura, ancho = imagen.shape[:2]
    altura_division = altura // num_divisiones
    divisiones = [
        imagen[i * altura_division:(i + 1) * altura_division, :]
        for i in range(num_divisiones)
    ]
    return divisiones
