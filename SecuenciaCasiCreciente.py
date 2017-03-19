#!/usr/bin/env python
# -*- coding: utf-8 -*-

def es_secuencia_casi_creciente(secuencia):
    # Este ejemplo está aquí solo para demostrar que un algoritmo de orden
    # cuadratico falla con creces la prueba 14. Es imposible recorrer 10 mil
    # millones de elementos en 4 segundos. :)
    length = len(secuencia)
    for i in range(length):
        for j in range(length):
            pass
    return False

################################################################################
#                         Código para probar solución                          #
################################################################################

from multiprocessing import Process, Value
from ctypes import c_bool

def f(secuencia, resultado):
    resultado.value = es_secuencia_casi_creciente(secuencia)

# Esta clase representa el resultado de ejecutar un caso de prueba
class ResultadoPrueba:
    def __init__(self, prueba, resultado_obtenido, excedio_tiempo):
        self.secuencia = prueba.secuencia
        self.resultado_esperado = prueba.resultado_esperado
        self.resultado_obtenido = resultado_obtenido
        self.excedio_tiempo = excedio_tiempo

    def exito(self):
        if self.excedio_tiempo:
            return False
        return self.resultado_esperado is self.resultado_obtenido

    def __str__(self):
        cadena = ""

        if len(self.secuencia) <= 15:
            cadena += "Secuencia: " + str(self.secuencia)
        else:
            cadena += "Longitud de la secuencia: "
            cadena += str(len(self.secuencia))
        cadena += "\n"
        if not self.excedio_tiempo:
            cadena += "Resultado esperado: " + str(self.resultado_esperado)
            cadena += "\n"
            cadena += "Resultado obtenido: " + str(self.resultado_obtenido)
        else:
            cadena += "La prueba excedió el tiempo máximo de ejecución."

        return cadena

# Esta clase representa un caso de prueba
class CasoDePrueba:
    def __init__(self, secuencia, resultado_esperado):
        self.secuencia = secuencia
        self.resultado_esperado = resultado_esperado

    # Este metodo ejecuta la prueba en un nuevo proceso.
    # Si la prueba excede el tiempo limite, mata el proceso y falla la prueba.
    def ejecutar(self):
        excedio_tiempo = False

        resultado = Value(c_bool, False)
        p = Process(target=f, args=(self.secuencia, resultado))
        p.start()
        p.join(4)

        if p.exitcode < 0:
            excedio_tiempo = True
            p.terminate()

        return ResultadoPrueba(self, resultado.value, excedio_tiempo)

def preparar_pruebas():
    pruebas = []

    # 1
    secuencia = [1, 3, 2, 1]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 2
    secuencia = [1, 3, 2]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 3
    secuencia = [1, 2, 1, 2]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 4
    secuencia = [1, 4, 10, 4, 2]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 5
    secuencia = [10, 1, 2, 3, 4, 5]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 6
    secuencia = [1, 1, 1, 2, 3]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 7
    secuencia = [0, -2, 5, 6]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 8
    secuencia = [1, 2, 3, 4, 5, 3, 5, 6]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 9
    secuencia = [40, 50, 60, 10, 20, 30]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 10
    secuencia = [1, 1]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 11
    secuencia = [10, 1, 2, 3, 4, 5, 6, 1]
    resultado = False
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 12
    secuencia = [1, 2, 3, 4, 3, 6]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 13
    secuencia = [1, 2, 3, 4, 99, 5, 6]
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    # 14
    # Caso en que la secuencia tiene el maximo de elementos (100 mil)
    secuencia = []
    for i in range(10**5):
        secuencia.append(i)
    resultado = True
    prueba = CasoDePrueba(secuencia, resultado)
    pruebas.append(prueba)

    return pruebas

def ejecutar_pruebas(pruebas):
    total = len(pruebas)
    fallas = []

    for i in range(total):
        prueba = pruebas[i]
        resultado = prueba.ejecutar()
        if not resultado.exito():
            fallas.append((i + 1, resultado))

    total_fallas = len(fallas)
    if total_fallas > 0:
        for i in range(total_fallas):
            (indice, falla) = fallas[i]
            mensaje_falla = "Prueba #" + str(indice) + ":"
            mensaje_falla += "\t".join(("\n" + str(falla)).splitlines(True)))
            print(mensaje_falla)
            if i < total_fallas - 1:
                print("----------------")
    print("\nPruebas pasadas: " + str(total - total_fallas) + "/" + str(total))

if __name__ == "__main__":
    pruebas = preparar_pruebas()
    ejecutar_pruebas(pruebas)
