# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 13:09:39 2023

@author: n982515
"""

from pysat.solvers import Glucose3
from itertools import combinations
import glob
import os

def leer_archivo(archivo):
    with open(archivo, 'r') as file:
        lineas = file.readlines()
    
    servidores = [list(map(int, linea.strip().split(','))) for linea in lineas[1:4]]
    computadoras = [list(map(int, linea.strip().split(','))) for linea in lineas[4:14]]
    incompatibilidades = {i + 1: list(map(int, linea.strip().split(',')[1:])) for i, linea in enumerate(lineas[14:])}
    
    return servidores, computadoras, incompatibilidades

def agregar_restriccion_1(solver, computadoras):
    for comp in computadoras:
        solver.add_clause(comp[1:])

def agregar_restriccion_2(solver, mega_servidores):
    for mega_servidor in mega_servidores:
        solver.add_clause(mega_servidor)

def agregar_restriccion_3(solver, incompatibilidades):
    for comp, incompatibles in incompatibilidades.items():
        for servidor in incompatibles:
            solver.add_clause([-comp, -servidor])

def resolver_problema(servidores, computadoras, incompatibilidades):
    solver = Glucose3()
    
    # Restricción 1
    agregar_restriccion_1(solver, computadoras)
    
    # Restricción 2
    agregar_restriccion_2(solver, servidores)
    
    # Restricción 3
    agregar_restriccion_3(solver, incompatibilidades)
    
    resultado = solver.solve()
    
    if resultado:
        modelo = [i for i in range(1, len(computadoras) * len(servidores) + 1) if solver.get_model()[i - 1] > 0]
        print("Solución encontrada:")
        print(modelo)
        return modelo
    else:
        print("No se encontró solución.")
        return None


# Ejemplo de uso
source = r"C:\Users\n982515\Downloads\test"
type_of_file = "*.txt"
filenames = glob.glob(os.path.join(source, type_of_file))

for filename in filenames:
    servidores, computadoras, incompatibilidades = leer_archivo(filename)
    result = resolver_problema(servidores, computadoras, incompatibilidades)
    
    if result:
        print(f"Para el archivo: {os.path.split(filename)[1]} - Asignación de servidores: {result}")
    else:
        print(f"Para el archivo: {os.path.split(filename)[1]} - No se encontró una asignación válida.")

