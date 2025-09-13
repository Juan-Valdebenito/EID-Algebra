#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de Funciones Matemáticas - VERSIÓN MEJORADA
Proyecto Parte B - EID

Este programa permite analizar funciones matemáticas, calcular su dominio,
recorrido, intersecciones y generar gráficos profesionales.
"""

import sys
import os

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas."""
    dependencias = ['sympy', 'matplotlib', 'customtkinter']
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)
    
    if faltantes:
        print("Dependencias faltantes:")
        for dep in faltantes:
            print(f"   - {dep}")
        print("\nPara instalar las dependencias, ejecute:")
        print("   py -m pip install -r requirements.txt")
        print("\nO instale individualmente:")
        for dep in faltantes:
            print(f"   py -m pip install {dep}")
        return False
    
    return True

def main():
    """Función principal que inicia la aplicación."""
    print("Analizador de Funciones Matemáticas")
    print("=" * 40)
    
    # Verificar dependencias
    if not verificar_dependencias():
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    try:
        from interface import AnalizadorFuncionesApp
        print("Dependencias verificadas correctamente")
        print("Iniciando aplicación...")
        
        app = AnalizadorFuncionesApp()
        app.run()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Verifique que todos los archivos estén en su lugar.")
        input("Presione Enter para salir...")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main() 