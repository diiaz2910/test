#usando recursividad para buscar la cadena mas larga en matriz de cadenas

def cadena_mas_larga(matriz, fila=0, columna=0):
    if fila >= len(matriz):
        #caso base sin coincidencias
        return ""
    #condicional final de fila y paso a la siguiente
    if columna >= len(matriz[fila]):
        return cadena_mas_larga(matriz,fila +1, 0)
    #recursividad revisando el siguiente elemento
    siguiente = cadena_mas_larga(matriz, fila, columna + 1)
    actual = matriz[fila][columna]
    #comparacion de la actual con el siguiente 
    if len(actual) >= len(siguiente):
        return actual
    else:
        return siguiente
    
matriz = [
    ["hola", "mundo", "python"],
]

print(cadena_mas_larga(matriz))