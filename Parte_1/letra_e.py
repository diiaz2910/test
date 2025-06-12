
#usando recursividad para encontrar palabras con la letra e en el centro
def letra_e(arreglo, indice=0):
    if indice >= len (arreglo):
        #se devuelve una lista vacia si no existen coincidencias 
        return []
    palabra_actual = arreglo[indice]
    longitud = len (palabra_actual)
    # se revisa que el resto de la cadena sea impar pues no existe el centro en una cadena par
    if longitud % 2 == 1:
        letra_central = palabra_actual[longitud // 2]
        if letra_central == "e":
            return [palabra_actual] + letra_e(arreglo, indice + 1)
    return letra_e(arreglo, indice + 1)


#datos de prueba
arreglo = [ "mesa", "huevo", "nieve" ]
resultado = letra_e(arreglo)
print("Palabras con e en el medio", resultado)