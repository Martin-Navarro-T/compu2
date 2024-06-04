from concurrent.futures import ThreadPoolExecutor

# Función que suma un valor a un número
def sumar(numero, valor):
    return numero + valor

# Lista de números de entrada
numeros = [1, 2, 3, 4, 5]

# Crea un ThreadPoolExecutor con un máximo de 2 hilos y lo asigna a la variable executor. 
# La cláusula with asegura que los recursos se liberen correctamente después de su uso.
with ThreadPoolExecutor(max_workers=2) as executor:
    # Utilizar el método map para aplicar la función sumar a cada elemento de la lista
    resultado = executor.map(sumar, numeros, [10] * len(numeros))

# Obtener los resultados en forma de lista
resultados_lista = list(resultado)

# Imprimir los resultados
print(resultados_lista) #[11, 12, 13, 14, 15]