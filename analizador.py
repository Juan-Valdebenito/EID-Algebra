"""
Módulo Analizador de Funciones Matemáticas
Proporciona funcionalidades para analizar funciones matemáticas:
- Dominio
- Recorrido  
- Intersecciones con los ejes
- Evaluación de puntos
"""

import sympy as sp
from sympy import symbols, solve, diff, limit, oo, S
from sympy.calculus.util import continuous_domain
import re
import math

class AnalizadorFunciones:
    """Clase principal para el análisis de funciones matemáticas."""
    
    def __init__(self):
        self.x = symbols('x')
        self.funcion = None
        self.funcion_sympy = None
        
    def parsear_funcion(self, expresion):
        """
        Convierte una expresión matemática en formato texto a una expresión SymPy.
        
        Args:
            expresion (str): Expresión matemática como string
            
        Returns:
            bool: True si se parseó correctamente, False en caso contrario
        """
        try:
            # Limpiar la expresión
            expresion = expresion.strip()
            
            # Reemplazar notaciones comunes
            expresion = expresion.replace('^', '**')
            expresion = expresion.replace('²', '**2')
            expresion = expresion.replace('³', '**3')
            
            # Manejar funciones trigonométricas
            expresion = re.sub(r'sin\b', 'sin', expresion)
            expresion = re.sub(r'cos\b', 'cos', expresion)
            expresion = re.sub(r'tan\b', 'tan', expresion)
            expresion = re.sub(r'log\b', 'log', expresion)
            expresion = re.sub(r'ln\b', 'log', expresion)
            expresion = re.sub(r'sqrt\b', 'sqrt', expresion)
            
            # Crear la expresión SymPy
            self.funcion_sympy = sp.sympify(expresion)
            self.funcion = expresion
            
            return True
            
        except Exception as e:
            # Solo mostrar errores en modo debug, no durante tests
            import sys
            if hasattr(sys, '_getframe') and 'test' not in sys._getframe(1).f_code.co_filename.lower():
                print(f"Error al parsear la función: {e}")
            return False
    
    def calcular_dominio(self):
        """
        Calcula el dominio de la función.
        
        Returns:
            str: Descripción del dominio
        """
        if self.funcion_sympy is None:
            return "No hay función definida"
            
        try:
            # Obtener el dominio continuo
            dominio = continuous_domain(self.funcion_sympy, self.x, S.Reals)
            
            if dominio == S.Reals:
                return "ℝ (Todos los números reales)"
            else:
                # Convertir notación técnica a formato legible
                dominio_str = str(dominio)
                
                # Reemplazar notaciones técnicas por versiones legibles
                if "Union" in dominio_str and "Interval.open" in dominio_str:
                    if "(-oo, 0)" in dominio_str and "(0, oo)" in dominio_str:
                        return "ℝ \\ {0} (Todos los reales excepto cero)"
                    elif "(-oo," in dominio_str:
                        # Extraer el punto de exclusión
                        import re
                        match = re.search(r'Interval\.open\((-?\d+(?:\.\d+)?), oo\)', dominio_str)
                        if match:
                            punto = match.group(1)
                            return f"({punto}, ∞) (Mayores que {punto})"
                
                if "Interval(0, oo)" in dominio_str:
                    return "[0, ∞) (Cero y números positivos)"
                elif "Interval.open(0, oo)" in dominio_str:
                    return "(0, ∞) (Solo números positivos)"
                elif "Interval(-oo, " in dominio_str:
                    # Extraer límite superior
                    import re
                    match = re.search(r'Interval\(-oo, (-?\d+(?:\.\d+)?)\)', dominio_str)
                    if match:
                        limite = match.group(1)
                        return f"(-∞, {limite}] (Menores o iguales que {limite})"
                
                # Si no se puede simplificar, mostrar versión más limpia
                dominio_limpio = dominio_str.replace("Interval.open", "").replace("Interval", "")
                dominio_limpio = dominio_limpio.replace("Union", "∪").replace("-oo", "-∞").replace("oo", "∞")
                return f"{dominio_limpio}"
                
        except Exception as e:
            return f"Error al calcular el dominio: {e}"
    
    def calcular_recorrido(self):
        """
        Calcula el recorrido de la función.
        
        Returns:
            str: Descripción del recorrido
        """
        if self.funcion_sympy is None:
            return "No hay función definida"
            
        try:
            # Para funciones polinómicas simples
            if self.funcion_sympy.is_polynomial():
                grado = sp.degree(self.funcion_sympy, self.x)
                if grado == 0:  # Función constante
                    return f"{{{self.funcion_sympy}}} (Función constante)"
                elif grado == 1:  # Función lineal
                    return "ℝ (Todos los números reales)"
                elif grado == 2:  # Función cuadrática
                    # Calcular el vértice
                    derivada = diff(self.funcion_sympy, self.x)
                    x_vertice = solve(derivada, self.x)[0]
                    y_vertice = self.funcion_sympy.subs(self.x, x_vertice)
                    
                    # Determinar si abre hacia arriba o abajo
                    coef_principal = self.funcion_sympy.coeff(self.x**2)
                    if coef_principal > 0:
                        return f"[{y_vertice}, ∞) (Desde el vértice hacia arriba)"
                    else:
                        return f"(-∞, {y_vertice}] (Desde el vértice hacia abajo)"
                else:
                    return "ℝ (Todos los números reales)"
            
            # Para otras funciones, intentar calcular límites
            try:
                lim_inf = limit(self.funcion_sympy, self.x, -oo)
                lim_sup = limit(self.funcion_sympy, self.x, oo)
                
                if lim_inf == lim_sup and lim_inf.is_finite:
                    return f"Recorrido: {{{lim_inf}}}"
                else:
                    return f"Recorrido: ({lim_inf}, {lim_sup})"
            except:
                return "Recorrido: No se pudo determinar automáticamente"
                
        except Exception as e:
            return f"Error al calcular el recorrido: {e}"
    
    def calcular_intersecciones(self):
        """
        Calcula las intersecciones de la función con los ejes X e Y.
        
        Returns:
            tuple: (intersecciones_x, interseccion_y) como valores numéricos
        """
        if self.funcion_sympy is None:
            return "No hay función definida", "No hay función definida"
            
        try:
            # Intersección con eje Y (x=0)
            try:
                y_val = self.funcion_sympy.subs(self.x, 0)
                # Verificar si el resultado es real y finito
                if y_val.is_real and y_val.is_finite:
                    interseccion_y = float(y_val)
                else:
                    interseccion_y = None
            except (TypeError, ValueError, AttributeError):
                interseccion_y = None
            
            # Intersecciones con eje X (y=0)
            intersecciones_x = []
            try:
                soluciones = solve(self.funcion_sympy, self.x)
                
                if soluciones:
                    for sol in soluciones:
                        try:
                            # Verificar múltiples condiciones para asegurar que es real
                            if (hasattr(sol, 'is_real') and sol.is_real and 
                                hasattr(sol, 'is_finite') and sol.is_finite):
                                # Intentar convertir a float de manera segura
                                float_val = complex(sol)
                                if abs(float_val.imag) < 1e-10:  # Prácticamente real
                                    intersecciones_x.append(float(float_val.real))
                        except (TypeError, ValueError, AttributeError, OverflowError):
                            # Si no se puede convertir, simplemente ignorar esta solución
                            continue
            except Exception as solve_error:
                print(f"Error al resolver ecuación: {solve_error}")
            
            return intersecciones_x, interseccion_y
            
        except Exception as e:
            print(f"Error general en cálculo de intersecciones: {e}")
            return [], None
    
    def evaluar_punto(self, x_valor):
        """
        Evalúa la función en un punto específico.
        
        Args:
            x_valor (float): Valor de x a evaluar
            
        Returns:
            tuple: (resultado, pasos)
        """
        if self.funcion_sympy is None:
            return None, "No hay función definida"
            
        try:
            # Calcular el resultado
            resultado = self.funcion_sympy.subs(self.x, x_valor)
            
            # Generar pasos de la evaluación
            pasos = []
            pasos.append(f"f({x_valor}) = {self.funcion}")
            pasos.append(f"Sustituyendo x = {x_valor}:")
            pasos.append(f"f({x_valor}) = {self.funcion_sympy.subs(self.x, x_valor)}")
            pasos.append(f"f({x_valor}) = {resultado}")
            
            return float(resultado), pasos
            
        except Exception as e:
            return None, f"Error al evaluar: {e}"
    
    def obtener_desarrollo_computacional(self):
        """
        Genera el desarrollo computacional paso a paso.
        
        Returns:
            list: Lista de pasos del desarrollo
        """
        if self.funcion_sympy is None:
            return ["No hay función definida"]
            
        pasos = []
        pasos.append("=== DESARROLLO COMPUTACIONAL ===")
        pasos.append(f"Función: f(x) = {self.funcion}")
        pasos.append("")
        
        # Dominio
        pasos.append("1. CÁLCULO DEL DOMINIO:")
        pasos.append(f"Dominio: {self.calcular_dominio()}")
        pasos.append("")
        
        # Recorrido
        pasos.append("2. CÁLCULO DEL RECORRIDO:")
        pasos.append(f"Recorrido: {self.calcular_recorrido()}")
        pasos.append("")
        
        # Intersecciones
        pasos.append("3. INTERSECCIONES CON LOS EJES:")
        int_x, int_y = self.calcular_intersecciones()
        
        # Formatear intersecciones X
        if isinstance(int_x, list) and int_x:
            intersecciones_x_str = ", ".join([f"({x}, 0)" for x in int_x])
            pasos.append(f"Con eje X: {intersecciones_x_str}")
        elif isinstance(int_x, list) and not int_x:
            pasos.append("Con eje X: No hay intersecciones reales")
        else:
            pasos.append(f"Con eje X: {int_x}")
        
        # Formatear intersección Y
        if int_y is not None:
            pasos.append(f"Con eje Y: (0, {int_y})")
        else:
            pasos.append("Con eje Y: No se pudo calcular")
        pasos.append("")
        
        # Derivada (si es posible)
        try:
            derivada = diff(self.funcion_sympy, self.x)
            pasos.append("4. DERIVADA:")
            pasos.append(f"f'(x) = {derivada}")
        except:
            pasos.append("4. DERIVADA: No se pudo calcular")
        
        return pasos
