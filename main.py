"""
Analizador de Funciones Matemáticas - EID
Archivo principal para ejecutar la aplicación.
"""

def main():
    """Función principal que ejecuta la interfaz gráfica."""
    
    print("🧮 Iniciando Analizador de Funciones Matemáticas...")
    print("📊 Proyecto EID - Análisis de Funciones")
    print("=" * 50)
    print("Iniciando Analizador de Funciones Matemáticas...")
    print("Proyecto EID - Análisis de Funciones")
    print("=" * 50)
    
    try:
        from interface import AnalizadorFuncionesApp
        print("Cargando interfaz gráfica...")
        app = AnalizadorFuncionesApp()
        app.run()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nInstale las dependencias necesarias:")
        print("   pip install sympy matplotlib customtkinter")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()