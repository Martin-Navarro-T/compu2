#Este código utiliza la concurrencia para probar si dos números son primos, 
# utilizando múltiples procesos en lugar de múltiples hilos. 
# Usa un ProcessPoolExecutor para ejecutar las pruebas de primalidad en paralelo 
# y luego imprime los resultados. 
# La función input() se utiliza para pausar la ejecución dentro de cada proceso hijo, 
# lo que te permite observar el PID de cada proceso que ejecuta prime_test.
from concurrent.futures import ProcessPoolExecutor
import os

def prime_test(num):
    #Imprime el ID de proceso del proceso principal.
    print('num: ', num, ' --- PID: ', os.getpid(), '  ')
    input()
    for i in range(2, abs(num)):
        if num%i == 0:
            return False
    return True

print('PID PADRE: ', os.getpid())
# Crear un ThreadPoolExecutor con, por ejemplo, 4 hilos
with ProcessPoolExecutor(max_workers=4) as executor:
    # Enviar tareas para su ejecución concurrente
    
    future1 = executor.submit(prime_test, 587)
    future2 = executor.submit(prime_test, 21)

    # Obtener los resultados cuando están listos
    result1 = future1.result()
    result2 = future2.result()
    
    print(result1)
    print(result2)

#El error que estás viendo, EOFError: EOF when reading a line, ocurre porque 
# la función input() está esperando una entrada del usuario, pero no puede 
# recibirla en un proceso hijo cuando se utiliza ProcessPoolExecutor. 
# A diferencia de ThreadPoolExecutor, donde todos los hilos comparten el mismo 
# espacio de memoria y pueden interactuar con la consola, los procesos hijos c
# reados por ProcessPoolExecutor tienen su propio espacio de memoria y no pueden 
# interactuar con la consola de la misma manera.

# Para solucionar este problema, deberás eliminar o modificar la línea input() 
# en la función prime_test. Aquí tienes el código modificado sin la pausa de input():