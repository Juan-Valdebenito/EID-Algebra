import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import sys
import os

# Importar módulos del proyecto
from analizador import AnalizadorFunciones
from graficador import GraficadorFunciones

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  
class AnalizadorFuncionesApp:
    
    def __init__(self):
        self.root = ctk.CTk()
        self.analizador = AnalizadorFunciones()
        self.graficador = GraficadorFunciones()
        self.canvas_actual = None
        self._running = True  # Flag para controlar si la app está activa
        
        self.configurar_ventana()
        self.crear_layout()
        self.configurar_atajos()
        
        # Configurar el protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
    def configurar_ventana(self):
     
        self.root.title("🧮 Analizador de Funciones Matemáticas - EID")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 900)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        
    def crear_layout(self):
        # Frame principal izquierdo (controles)
        self.frame_izquierdo = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.frame_izquierdo.grid_columnconfigure(0, weight=1)
        
        # Frame principal derecho (gráfico y resultados)
        self.frame_derecho = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame_derecho.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.frame_derecho.grid_rowconfigure(0, weight=2)
        self.frame_derecho.grid_rowconfigure(1, weight=1)
        self.frame_derecho.grid_columnconfigure(0, weight=1)
        
        self.crear_header()
        self.crear_controles()
        self.crear_area_grafico()
        self.crear_area_resultados()
        self.crear_footer()
        
    def crear_header(self):
        # Título principal
        self.titulo = ctk.CTkLabel(
            self.frame_izquierdo, 
            text=" Analizador de Funciones",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo.grid(row=0, column=0, pady=(20, 5), sticky="ew", columnspan=2)
        
        # Subtítulo
        self.subtitulo = ctk.CTkLabel(
            self.frame_izquierdo, 
            text="Análisis Matemático Completo",
            font=ctk.CTkFont(size=14),
            text_color=("gray70", "gray30")
        )
        self.subtitulo.grid(row=1, column=0, pady=(0, 20), sticky="ew", columnspan=2)
        
    def crear_controles(self):
        # Sección de entrada de función
        funcion_frame = ctk.CTkFrame(self.frame_izquierdo, corner_radius=10)
        funcion_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        funcion_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            funcion_frame, 
            text=" Función a Analizar",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), sticky="w", padx=15)
        
        ctk.CTkLabel(
            funcion_frame, 
            text="f(x) =",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=1, column=0, sticky="w", padx=15, pady=(0, 5))
        
        self.entry_funcion = ctk.CTkEntry(
            funcion_frame, 
            placeholder_text="Ingrese su función matemática...",
            font=ctk.CTkFont(size=14),
            height=35,
            corner_radius=8
        )
        self.entry_funcion.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))
        self.entry_funcion.bind('<Return>', lambda e: self.analizar_funcion())
        
        # Botón principal de análisis
        self.btn_analizar = ctk.CTkButton(
            funcion_frame,
            text=" Analizar Función",
            command=self.analizar_funcion,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#dc3545", "#8b0000"),  
            hover_color=("#b02a37", "#660000")
        )
        self.btn_analizar.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        # Sección de ejemplos
        ejemplos_frame = ctk.CTkFrame(self.frame_izquierdo, corner_radius=10)
        ejemplos_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))
        ejemplos_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        ctk.CTkLabel(
            ejemplos_frame, 
            text=" Ejemplos Rápidos:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=4, pady=(15, 10))
        
        ejemplos = [
            ("x²+2x+1", "x**2 + 2*x + 1"),
            ("x³-3x+2", "x**3 - 3*x + 2"),
            ("sin(x)", "sin(x)"),
            ("1/x", "1/x"),
            ("√x", "sqrt(x)"),
            ("exp(x)", "exp(x)"),
            ("log(x)", "log(x)"),
            ("cos(x)", "cos(x)")
        ]
        
        # Primera fila de ejemplos
        for i in range(4):
            texto, funcion = ejemplos[i]
            btn = ctk.CTkButton(
                ejemplos_frame,
                text=texto,
                command=lambda f=funcion: self.cargar_ejemplo(f),
                width=70,
                height=28,
                font=ctk.CTkFont(size=11),
                fg_color=("#6c757d", "#495057"),
                hover_color=("#5a6268", "#343a40")
            )
            btn.grid(row=1, column=i, padx=3, pady=(0, 5))
        
        # Segunda fila de ejemplos
        for i in range(4):
            if i + 4 < len(ejemplos):
                texto, funcion = ejemplos[i + 4]
                btn = ctk.CTkButton(
                    ejemplos_frame,
                    text=texto,
                    command=lambda f=funcion: self.cargar_ejemplo(f),
                    width=70,
                    height=28,
                    font=ctk.CTkFont(size=11),
                    fg_color=("#6c757d", "#495057"),
                    hover_color=("#5a6268", "#343a40")
                )
                btn.grid(row=2, column=i, padx=3, pady=(0, 15))
        
        # Sección de evaluación
        evaluacion_frame = ctk.CTkFrame(self.frame_izquierdo, corner_radius=10)
        evaluacion_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        evaluacion_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            evaluacion_frame, 
            text=" Evaluar en punto:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, columnspan=3, pady=(15, 10), sticky="w", padx=15)
        
        ctk.CTkLabel(evaluacion_frame, text="x =").grid(row=1, column=0, padx=(15, 5), sticky="e")
        
        self.entry_valor = ctk.CTkEntry(
            evaluacion_frame,
            placeholder_text="Ej: 2",
            width=100,
            font=ctk.CTkFont(size=12)
        )
        self.entry_valor.grid(row=1, column=1, padx=5, sticky="w")
        self.entry_valor.bind('<Return>', lambda e: self.evaluar_punto())
        
        self.btn_evaluar = ctk.CTkButton(
            evaluacion_frame,
            text=" Evaluar",
            command=self.evaluar_punto,
            width=80,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color=("#dc3545", "#8b0000"),  
            hover_color=("#b02a37", "#660000")
        )
        self.btn_evaluar.grid(row=1, column=2, padx=(5, 15), pady=(0, 15))
        
        # Botones de acción
        botones_frame = ctk.CTkFrame(self.frame_izquierdo, corner_radius=10)
        botones_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        botones_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.btn_limpiar = ctk.CTkButton(
            botones_frame,
            text=" Limpiar ",
            command=self.limpiar_todo,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=("#6c757d", "#495057"),  
            hover_color=("#5a6268", "#343a40")
        )
        self.btn_limpiar.grid(row=0, column=0, padx=(15, 5), pady=15, sticky="ew")
        
        self.btn_ayuda = ctk.CTkButton(
            botones_frame,
            text="❓ Ayuda",
            command=self.mostrar_ayuda,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=("#17a2b8", "#138496"),  
            hover_color=("#138496", "#0f6674")
        )
        self.btn_ayuda.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="ew")
        
    def crear_area_grafico(self):
        """Crea el área para mostrar el gráfico con diseño moderno."""
        grafico_frame = ctk.CTkFrame(self.frame_derecho, corner_radius=10)
        grafico_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        grafico_frame.grid_rowconfigure(1, weight=1)
        grafico_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            grafico_frame, 
            text=" Gráfico de la Función",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), sticky="w", padx=15)
        
        self.canvas_grafico = tk.Canvas(
            grafico_frame, 
            bg="white",
            relief="flat",
            borderwidth=0
        )
        self.canvas_grafico.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
    def crear_area_resultados(self):
        """Crea el área para mostrar los resultados con diseño moderno."""
        resultados_frame = ctk.CTkFrame(self.frame_derecho, corner_radius=10)
        resultados_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        resultados_frame.grid_rowconfigure(1, weight=1)
        resultados_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            resultados_frame, 
            text=" Análisis y Resultados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, pady=(15, 10), sticky="w", padx=15)
        
        self.text_resultados = scrolledtext.ScrolledText(
            resultados_frame, 
            height=12, 
            font=("Consolas", 11),
            wrap=tk.WORD,
            bg="#2b2b2b",
            fg="white",
            relief="flat",
            borderwidth=0,
            insertbackground="white"
        )
        self.text_resultados.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
    def crear_footer(self):
        """Crea el pie de página con información del proyecto."""
        footer_frame = ctk.CTkFrame(self.frame_izquierdo, corner_radius=10)
        footer_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 20))
        
        info_text = "Proyecto EID - Análisis de Funciones\nDesarrollado por el grupo N°7"
        ctk.CTkLabel(
            footer_frame, 
            text=info_text,
            font=ctk.CTkFont(size=11),
            text_color=("gray60", "gray40"),
            justify="center"
        ).grid(row=0, column=0, pady=15)
        
    def configurar_atajos(self):
        """Configura atajos de teclado."""
        self.root.bind('<Control-a>', lambda e: self.analizar_funcion())
        self.root.bind('<Control-e>', lambda e: self.evaluar_punto())
        self.root.bind('<Control-l>', lambda e: self.limpiar_todo())
        self.root.bind('<F1>', lambda e: self.mostrar_ayuda())
        
    def cargar_ejemplo(self, ejemplo):
        """Carga un ejemplo de función en el campo de entrada."""
        if not self._running:  # No ejecutar si la app se está cerrando
            return
            
        self.entry_funcion.delete(0, tk.END)
        self.entry_funcion.insert(0, ejemplo)
        self.entry_funcion.focus()
        
    def analizar_funcion(self):
        if not self._running:  # No ejecutar si la app se está cerrando
            return
            
        try:
            funcion_str = self.entry_funcion.get().strip()
            if not funcion_str:
                messagebox.showwarning("⚠️ Advertencia", "Por favor ingrese una función.")
                return
            
            if not self.analizador.parsear_funcion(funcion_str):
                messagebox.showerror("❌ Error", "Función inválida. Revise la sintaxis.")
                return
            
            # Limpiar resultados anteriores
            self.text_resultados.delete(1.0, tk.END)
            
            # Análisis completo
            dominio = self.analizador.calcular_dominio()
            recorrido = self.analizador.calcular_recorrido()
            desarrollo = self.analizador.obtener_desarrollo_computacional()
            
            # Mostrar resultados
            resultados = [
                " ANÁLISIS COMPLETO DE LA FUNCIÓN",
                "=" * 50,
                f" Función: f(x) = {funcion_str}",
                "",
                f" Dominio: {dominio}",
                f" Recorrido: {recorrido}",
                "",
                " DESARROLLO COMPUTACIONAL:",
                "-" * 30
            ]
            
            resultados.extend(desarrollo)
            
            for resultado in resultados:
                self.text_resultados.insert(tk.END, resultado + "\n")
            
            # Crear gráfico
            self.crear_grafico()
            
            if self._running:  # Solo mostrar mensaje si la app sigue activa
                messagebox.showinfo("La funcion se analizo correctamente.")
            
        except Exception as e:
            print(f"Error en análisis: {e}")
            if self._running:
                messagebox.showerror(" Error", f" analizar la función: {str(e)}")
    
    def evaluar_punto(self):

        if not self._running:  # No ejecutar si la app se está cerrando
            return
            
        try:
            if not hasattr(self.analizador, 'funcion_sympy') or self.analizador.funcion_sympy is None:
                messagebox.showwarning(" Advertencia", "Primero debe analizar una función.")
                return
            
            valor_str = self.entry_valor.get().strip()
            if not valor_str:
                messagebox.showwarning(" Advertencia", "Por favor ingrese un valor para evaluar.")
                return
            
            try:
                x_val = float(valor_str)
            except ValueError:
                messagebox.showerror(" Error", "Ingrese un número válido.")
                return
            
            resultado, pasos = self.analizador.evaluar_punto(x_val)
            
            if resultado is not None:
                # Mostrar pasos en el área de resultados
                self.text_resultados.insert(tk.END, f"\n EVALUACIÓN EN x = {x_val}\n")
                self.text_resultados.insert(tk.END, "=" * 30 + "\n")
                
                if isinstance(pasos, list):
                    for paso in pasos:
                        self.text_resultados.insert(tk.END, paso + "\n")
                else:
                    self.text_resultados.insert(tk.END, str(pasos) + "\n")
                
                self.text_resultados.insert(tk.END, f"\n Resultado: f({x_val}) = {resultado}\n")
                
                # Crear gráfico con el punto evaluado
                self.crear_grafico(punto_evaluado=(x_val, resultado))
                
                if self._running:  # Solo mostrar mensaje si la app sigue activa
                    messagebox.showinfo(" Éxito", f"f({x_val}) = {resultado}")
            else:
                error_msg = pasos if isinstance(pasos, str) else "Error al evaluar el punto"
                if self._running:
                    messagebox.showerror(" Error", error_msg)
                
        except Exception as e:
            print(f"Error en evaluación: {e}")
            if self._running:
                messagebox.showerror(" Error", f"Error al evaluar el punto: {str(e)}")
            
    def crear_grafico(self, punto_evaluado=None):
        """Crea y muestra el gráfico de la función."""
        if not self._running:  
            return
            
        try:
            # Limpiar matplotlib completamente primero
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # Limpiar canvas anterior de manera más segura
            if hasattr(self, 'canvas_actual') and self.canvas_actual is not None:
                try:
                    widget = self.canvas_actual.get_tk_widget()
                    # Verificar que el widget aún existe y es válido
                    if hasattr(widget, 'winfo_exists'):
                        try:
                            if widget.winfo_exists():
                                widget.pack_forget()  # Primero quitar del layout
                                widget.destroy()      # Luego destruir
                        except tk.TclError:
                            pass
                except (AttributeError, tk.TclError):
                    pass
                finally:
                    self.canvas_actual = None
            
            # Limpiar el canvas tkinter con protección mejorada
            try:
                if hasattr(self, 'canvas_grafico'):
                    try:
                        if self.canvas_grafico.winfo_exists():
                            self.canvas_grafico.delete("all")
                    except tk.TclError:
                        pass
            except (AttributeError, tk.TclError):
                pass
            
            int_x, int_y = self.analizador.calcular_intersecciones()
            
            fig = self.graficador.crear_grafico(
                funcion_sympy=self.analizador.funcion_sympy,
                x_range=(-10, 10),
                intersecciones_x=int_x,
                interseccion_y=int_y,
                punto_evaluado=punto_evaluado,
                titulo=f"f(x) = {self.analizador.funcion}"
            )
            
            if fig and self._running:  # Solo mostrar si la app sigue activa
                try:
                    if hasattr(self, 'canvas_grafico') and self.canvas_grafico.winfo_exists():
                        self.canvas_actual = FigureCanvasTkAgg(fig, self.canvas_grafico)
                        self.canvas_actual.draw()
                        self.canvas_actual.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                except Exception as e:
                    print(f"Error al mostrar gráfico: {e}")
                
        except Exception as e:
            print(f"Error al crear gráfico: {e}")
            
    def limpiar_todo(self):
        """Limpia todos los campos y resultados."""
        if not self._running:  # No limpiar si la app se está cerrando
            return
            
        try:
            # Limpiar campos de entrada con protección
            try:
                if hasattr(self, 'entry_funcion'):
                    self.entry_funcion.delete(0, tk.END)
            except (AttributeError, tk.TclError):
                pass
                
            try:
                if hasattr(self, 'entry_valor'):
                    self.entry_valor.delete(0, tk.END)
            except (AttributeError, tk.TclError):
                pass
                
            try:
                if hasattr(self, 'text_resultados'):
                    self.text_resultados.delete(1.0, tk.END)
            except (AttributeError, tk.TclError):
                pass
            
            # CORRECCIÓN: Limpiar canvas con máxima protección
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
                
            if hasattr(self, 'canvas_actual') and self.canvas_actual is not None:
                try:
                    widget = self.canvas_actual.get_tk_widget()
                    if hasattr(widget, 'winfo_exists'):
                        try:
                            if widget.winfo_exists():
                                widget.pack_forget()
                                widget.destroy()
                        except tk.TclError:
                            pass
                except (AttributeError, tk.TclError):
                    pass
                finally:
                    self.canvas_actual = None
            
            try:
                if hasattr(self, 'canvas_grafico'):
                    try:
                        if self.canvas_grafico.winfo_exists():
                            self.canvas_grafico.delete("all")
                    except tk.TclError:
                        pass
            except (AttributeError, tk.TclError):
                pass
            
            try:
                if hasattr(self, 'graficador'):
                    self.graficador.limpiar_grafico()
            except (AttributeError, Exception):
                pass
            
            if self._running:  # Solo mostrar mensaje si la app sigue activa
                messagebox.showinfo(" Limpiado", "Todos los campos han sido limpiados.")
            
        except Exception as e:
            print(f"Error al limpiar: {e}")
            try:
                if self._running:
                    messagebox.showinfo(" Limpiado", "Campos limpiados (con errores menores)")
            except:
                pass
                
    def mostrar_ayuda(self):
        """Muestra una ventana de ayuda."""
        if not self._running:  # No mostrar ayuda si la app se está cerrando
            return
            
        ayuda_texto = """ANALIZADOR DE FUNCIONES MATEMÁTICAS

CÓMO USAR:
1. Ingrese una función en el campo "f(x) ="
2. Haga clic en "Analizar Función"
3. Opcionalmente, evalúe en un punto específico

 EJEMPLOS DE FUNCIONES:
• Polinómicas: x**2 + 2*x + 1
• Trigonométricas: sin(x), cos(x)
• Exponenciales: exp(x), 2**x
• Logarítmicas: log(x), ln(x)
• Racionales: 1/x, (x+1)/(x-1)
• Radicales: sqrt(x), x**(1/3)

ATAJOS DE TECLADO:
• Ctrl+A: Analizar función
• Ctrl+E: Evaluar punto
• Ctrl+L: Limpiar todo
• F1: Mostrar esta ayuda

NOTACIÓN:
• Use ** para potencias (x**2)
• Use * para multiplicación (2*x)
• Use paréntesis para agrupar
• Use funciones estándar (sin, cos, log, etc.)"""
        
        messagebox.showinfo(" Ayuda", ayuda_texto)
        
    def cerrar_aplicacion(self):
        """Maneja el cierre de la aplicación de manera limpia."""
        self._running = False
        
        try:
            # Cancelar todos los callbacks pendientes de CustomTkinter
            if hasattr(self.root, '_after_ids'):
                for after_id in getattr(self.root, '_after_ids', []):
                    try:
                        self.root.after_cancel(after_id)
                    except:
                        pass
            
            # Limpiar matplotlib canvas
            if hasattr(self, 'canvas_actual') and self.canvas_actual is not None:
                try:
                    widget = self.canvas_actual.get_tk_widget()
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        widget.destroy()
                except:
                    pass
                self.canvas_actual = None
            
            # Limpiar gráficos de matplotlib
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # Limpiar graficador
            if hasattr(self, 'graficador'):
                try:
                    self.graficador.limpiar_grafico()
                except:
                    pass
            
            # Destruir ventana principal de manera segura
            try:
                # Primero quit para salir del mainloop
                self.root.quit()
                # Pequeña pausa para permitir limpieza
                self.root.update_idletasks()
                # Luego destroy
                self.root.destroy()
            except:
                pass
                
        except Exception as e:
            # En caso de error crítico, forzar salida
            import sys
            sys.exit(0)
        
    def run(self):
        """Ejecuta la aplicación."""
        try:
            # Configurar posición centrada de manera segura
            try:
                self.root.update_idletasks()
                x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
                y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
                self.root.geometry(f"+{x}+{y}")
            except:
                # Si falla el centrado, usar posición por defecto
                pass
            
            # Configurar manejo de cierre de ventana
            self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
            
            # Ejecutar mainloop con manejo de errores
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("Aplicación interrumpida por el usuario")
            self.cerrar_aplicacion()
        except Exception as e:
            print(f"Error durante ejecución: {e}")
            self.cerrar_aplicacion()
        finally:
            self._running = False
            # Asegurar limpieza final
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass

if __name__ == "__main__":
    app = AnalizadorFuncionesApp()
    app.run() 