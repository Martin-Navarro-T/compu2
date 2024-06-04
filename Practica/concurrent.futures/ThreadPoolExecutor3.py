from concurrent.futures import ThreadPoolExecutor

# Función que toma un número y devuelve su cuadrado
def calcular_cuadrado(numero):
    return numero ** 2

#Crea un ThreadPoolExecutor con un máximo de 2 hilos y lo asigna a la variable executor. 
# La cláusula with asegura que los recursos se liberen correctamente después de su uso.
with ThreadPoolExecutor(max_workers=2) as executor:
    # Enviar una tarea para calcular el cuadrado de 5
    future_resultado = executor.submit(calcular_cuadrado, 5)

    # Verificar si la tarea ha finalizado
    if future_resultado.done():
        resultado = future_resultado.result()  # Obtener el resultado
        print(f"Resultado: {resultado}")
    else:
        print("La tarea aún no ha finalizado. Esperando...")

# Verificar nuevamente si la tarea ha finalizado
if future_resultado.done():
    resultado = future_resultado.result()
    print(f"Resultado final: {resultado}")