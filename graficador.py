"""
Módulo Graficador de Funciones Matemáticas
Usa matplotlib + sympy para graficar funciones con:
- Ejes claramente etiquetados
- Intersecciones con X e Y
- Punto evaluado destacado
"""

import matplotlib.pyplot as plt
import sympy as sp

class GraficadorFunciones:
    """Clase para graficar funciones simbólicas con Matplotlib."""

    def __init__(self):
        self.figura = None
        self.ejes = None

    def crear_grafico(self, funcion_sympy, x_range=(-10, 10),
                      intersecciones_x=None, interseccion_y=None,
                      punto_evaluado=None, titulo="Gráfico de f(x)"):
        """
        Genera un gráfico de la función.
        
        Args:
            funcion_sympy (sympy.Expr): función en formato SymPy
            x_range (tuple): rango de valores en X
            intersecciones_x (list): valores de x donde f(x)=0
            interseccion_y (float): valor de f(0)
            punto_evaluado (tuple): coordenada (x,y) evaluada
            titulo (str): título del gráfico
        
        Returns:
            matplotlib.figure.Figure: figura generada
        """
        try:
            # Crear nueva figura
            self.figura, self.ejes = plt.subplots(figsize=(7, 5))
            
            # Generar valores X sin numpy (solo lista de floats)
            xs = [i/10 for i in range(x_range[0]*10, x_range[1]*10 + 1)]
            ys = []
            for val in xs:
                try:
                    y_val = float(funcion_sympy.subs(sp.Symbol('x'), val))
                    if abs(y_val) < 1e6:  # limitar valores absurdos
                        ys.append(y_val)
                    else:
                        ys.append(None)
                except:
                    ys.append(None)

            # Graficar la curva principal
            self.ejes.plot(xs, ys, label=f"f(x) = {funcion_sympy}", color="blue")

            # Intersecciones en X
            if intersecciones_x:
                for x0 in intersecciones_x:
                    self.ejes.scatter(x0, 0, color="red", s=60, marker="o", label="Intersección X")

            # Intersección en Y
            if interseccion_y is not None:
                self.ejes.scatter(0, interseccion_y, color="green", s=60, marker="o", label="Intersección Y")

            # Punto evaluado
            if punto_evaluado is not None:
                self.ejes.scatter(punto_evaluado[0], punto_evaluado[1],
                                  color="orange", s=80, marker="x", label=f"Punto ({punto_evaluado[0]}, {punto_evaluado[1]})")

            # Ejes y formato
            self.ejes.axhline(0, color="black", linewidth=1)
            self.ejes.axvline(0, color="black", linewidth=1)

            self.ejes.set_title(titulo, fontsize=14, fontweight="bold")
            self.ejes.set_xlabel("Eje X")
            self.ejes.set_ylabel("Eje Y")
            self.ejes.grid(True, linestyle="--", alpha=0.6)
            self.ejes.legend(loc="best", fontsize=9)

            self.figura.tight_layout()
            return self.figura

        except Exception as e:
            print(f"Error al crear gráfico: {e}")
            return None

    def limpiar_grafico(self):
        """Cierra la figura activa para liberar memoria."""
        try:
            plt.close(self.figura)
            self.figura = None
            self.ejes = None
        except:
            pass
