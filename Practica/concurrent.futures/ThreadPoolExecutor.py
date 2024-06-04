# Este código utiliza la concurrencia para probar si dos números son primos. 
# Usa un ThreadPoolExecutor para ejecutar las pruebas de primalidad en paralelo 
# y luego imprime los resultados.
from concurrent.futures import ThreadPoolExecutor
import os

def prime_test(num):
    #Imprime el número que se está probando (num) y el ID de proceso (PID) del proceso actual.
    print('num: ', num, ' --- PID: ', os.getpid(), '  ')
    for i in range(2, abs(num)):
        if num%i == 0:
            return False
    return True

#Imprime el ID de proceso del proceso principal.
print('PID PADRE: ', os.getpid())

# Crear un ThreadPoolExecutor con, por ejemplo, 4 hilos
# Crea un ThreadPoolExecutor con un máximo de 4 hilos y lo asigna a la variable executor. 
# La cláusula with asegura que los recursos se liberen correctamente después de su uso.
with ThreadPoolExecutor(max_workers=4) as executor:
    # Enviar tareas para su ejecución concurrente
    #Envía la tarea de probar si 587 es primo a la pool de hilos 
    # y guarda el objeto Future resultante en future1.
    future1 = executor.submit(prime_test, 587)
    #Envía la tarea de probar si 21 es primo a la pool de hilos 
    # y guarda el objeto Future resultante en future2.
    future2 = executor.submit(prime_test, 21)
    
    # Obtener los resultados cuando están listos
    result1 = future1.result()
    result2 = future2.result()
    
    print(result1)
    print(result2)
    
#SALIDA
#    PID PADRE:  15236
#    num:  587  --- PID:  15236   
#    num:  21  --- PID:  15236   
#    True
#    False