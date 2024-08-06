import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import procesamiento_imagen as pi 
import signal

def ejecutar():
    # Coordina la ejecución del procesamiento de imágenes: carga, división, procesamiento y unión.

    root = tk.Tk()
    root.withdraw()

    # Primero, solicitar al usuario que seleccione la imagen
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png")])
    if not file_path:
        messagebox.showerror("Error", "No se seleccionó ninguna imagen.")
        return
    
    imagen, ancho, altura = pi.cargar_imagen(file_path)

    # Luego, solicitar al usuario el directorio para guardar la imagen
    directorio_guardado = filedialog.askdirectory(title="Selecciona el directorio para guardar la imagen")
    if not directorio_guardado:
        messagebox.showerror("Error", "No se seleccionó ningún directorio para guardar la imagen.")
        return

    # Solicitar al usuario el nombre del archivo
    nombre_archivo = simpledialog.askstring("Nombre del archivo", "Ingresa el nombre del archivo (sin extensión):")
    if not nombre_archivo:
        messagebox.showerror("Error", "No se ingresó ningún nombre para el archivo.")
        return
    
    # Construir la ruta completa para guardar la imagen
    ruta_guardado = f"{directorio_guardado}/{nombre_archivo}.jpg"

    procesos = []
    signal.signal(signal.SIGINT, lambda signum, frame: pi.limpiar(signum, frame, procesos))

    divisiones_procesadas, ancho = pi.procesar_imagen(imagen)
    pi.unir_imagenes(divisiones_procesadas, ancho, ruta_guardado)

    # Mostrar mensaje de confirmación
    messagebox.showinfo("Éxito", f"Imagen procesada guardada como: {ruta_guardado}")

if __name__ == '__main__':
    ejecutar()
