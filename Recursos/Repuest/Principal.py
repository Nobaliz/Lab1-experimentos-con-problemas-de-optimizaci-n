import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.sparse import csr_matrix

# Algoritmo de optimización de dos variables
class OptimizacionDosVariables(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        # Función de costo
        tk.Label(self, text="Función de costo (en términos de x y):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_funcion = tk.Entry(self, width=30)
        self.entrada_funcion.grid(row=0, column=1, padx=5, pady=5)

        # Restricción
        tk.Label(self, text="Restricción (x + y ≤ ):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_restriccion = tk.Entry(self, width=10)
        self.entrada_restriccion.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Escala X (min):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.escala_x_min = tk.Entry(self, width=5)
        self.escala_x_min.insert(0, "0")
        self.escala_x_min.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Escala X (max):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.escala_x_max = tk.Entry(self, width=5)
        self.escala_x_max.insert(0, "5")
        self.escala_x_max.grid(row=3, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Escala Y (min):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.escala_y_min = tk.Entry(self, width=5)
        self.escala_y_min.insert(0, "0")
        self.escala_y_min.grid(row=4, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Escala Y (max):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.escala_y_max = tk.Entry(self, width=5)
        self.escala_y_max.insert(0, "5")
        self.escala_y_max.grid(row=5, column=1, padx=5, pady=5)
        
        self.boton_graficar = tk.Button(self, text="Graficar", command=self.graficar_region_factible)
        self.boton_graficar.grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Label(self, text="Valor de X:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.entrada_x = tk.Entry(self, width=10)
        self.entrada_x.insert(0, "0")
        self.entrada_x.grid(row=7, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Valor de Y:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.entrada_y = tk.Entry(self, width=10)
        self.entrada_y.insert(0, "0")
        self.entrada_y.grid(row=8, column=1, padx=5, pady=5)
        
        self.etiqueta_resultado = tk.Label(self, text="Resultado: ")
        self.etiqueta_resultado.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        
    def calcular_funcion_costo(self):
        try:
            funcion_costo = self.entrada_funcion.get()
            valores = {'x': float(self.entrada_x.get()), 'y': float(self.entrada_y.get())}
            resultado = eval(funcion_costo, {}, valores)
            self.etiqueta_resultado.config(text=f"Resultado: {resultado:.2f}")
        except Exception as e:
            self.etiqueta_resultado.config(text="Error en la función")
    
    def graficar_region_factible(self):
        try:
            funcion_costo = self.entrada_funcion.get()
            restriccion = float(self.entrada_restriccion.get())
            
            plt.clf()

            x_min = float(self.escala_x_min.get())
            x_max = float(self.escala_x_max.get())
            y_min = float(self.escala_y_min.get())
            y_max = float(self.escala_y_max.get())

            x = np.linspace(x_min, x_max, 400)
            y = np.linspace(y_min, y_max, 400)
            X, Y = np.meshgrid(x, y)
            Z = eval(funcion_costo, {}, {'x': X, 'y': Y})

            plt.contour(X, Y, Z, levels=50, cmap='jet')
            plt.colorbar(label='Costo')

            plt.fill_between(x, 0, restriccion - x, where=(x <= restriccion), color='gray', alpha=0.5)
            plt.axhline(0, color='black', linewidth=1.5)
            plt.axvline(0, color='black', linewidth=1.5)

            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Región Factible y Función de Costo ({x_min} ≤ x ≤ {x_max})')
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", "Error al graficar")

# Representación de matrices sparse
class MatricesSparse(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self, text="Ingrese la matriz densa (en formato lista de listas):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_matriz = tk.Entry(self, width=30)
        self.entrada_matriz.grid(row=0, column=1, padx=5, pady=5)
        
        self.boton_calcular = tk.Button(self, text="Convertir a CSR", command=self.convertir_a_csr)
        self.boton_calcular.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.etiqueta_resultado = tk.Label(self, text="Resultados: ")
        self.etiqueta_resultado.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    def convertir_a_csr(self):
        try:
            matriz_densa = eval(self.entrada_matriz.get())
            if not isinstance(matriz_densa, (list, np.ndarray)) or not all(isinstance(i, (list, np.ndarray)) for i in matriz_densa):
                raise ValueError("La entrada debe ser una lista de listas o un array.")
            
            # Método CSR manual
            def csr_method(matrix):
                data = []
                ind_col = []
                indptr = [0]
                nnz = 0

                for i in matrix:
                    for j, val in enumerate(i):
                        if val != 0:
                            data.append(val)
                            ind_col.append(j)
                            nnz += 1
                    indptr.append(nnz)
                return np.array(data), np.array(ind_col), np.array(indptr)

            data, ind_col, indptr = csr_method(matriz_densa)
            
            # CSR usando Scipy
            matriz_sparse = csr_matrix(matriz_densa)
            
            self.etiqueta_resultado.config(text=f'Matriz densa: {matriz_densa}\n'
                                                f'Datos CSR: {data}\n'
                                                f'Índices columna CSR: {ind_col}\n'
                                                f'Cambio en fila CSR: {indptr}\n\n'
                                                f'Valores CSR de Scipy: {matriz_sparse.data}\n'
                                                f'Índices columna CSR de Scipy: {matriz_sparse.indices}\n'
                                                f'Cambio en fila CSR de Scipy: {matriz_sparse.indptr}')
        except Exception as e:
            messagebox.showerror("Error", "Error al procesar la matriz")

# Expansión en series de Taylor
class ExpansionTaylor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self, text="Seleccionar función:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.funcion_var = tk.IntVar()
        funciones = [("Seno", 1), ("Coseno", 2), ("Exponencial", 3), ("Logarítmica", 4), ("Polinómica", 5)]
        for texto, valor in funciones:
            tk.Radiobutton(self, text=texto, variable=self.funcion_var, value=valor).grid(row=0, column=valor, padx=5, pady=5)

        tk.Label(self, text="Número de términos:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_terminos = tk.Entry(self, width=10)
        self.entrada_terminos.insert(0, "5")
        self.entrada_terminos.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Punto de expansión:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entrada_punto = tk.Entry(self, width=10)
        self.entrada_punto.insert(0, "0")
        self.entrada_punto.grid(row=2, column=1, padx=5, pady=5)
        
        self.boton_graficar = tk.Button(self, text="Graficar", command=self.graficar_expansion)
        self.boton_graficar.grid(row=3, column=0, columnspan=2, pady=10)
        
    def graficar_expansion(self):
        try:
            funcion = self.funcion_var.get()
            terminos = int(self.entrada_terminos.get())
            punto = float(self.entrada_punto.get())
            
            x = sp.Symbol('x')
            if funcion == 1:
                f = sp.sin(x)
            elif funcion == 2:
                f = sp.cos(x)
            elif funcion == 3:
                f = sp.exp(x)
            elif funcion == 4:
                f = sp.log(x)
            elif funcion == 5:
                f = x**3 - 2*x**2 + x - 1
            else:
                raise ValueError("Función no reconocida")
            
            taylor_exp = sp.series(f, x, punto, terminos).removeO()
            
            f_lambdified = sp.lambdify(x, f, "numpy")
            taylor_exp_lambdified = sp.lambdify(x, taylor_exp, "numpy")
            
            x_vals = np.linspace(punto - 2, punto + 2, 400)
            f_vals = f_lambdified(x_vals)
            taylor_vals = taylor_exp_lambdified(x_vals)
            
            plt.figure()
            plt.plot(x_vals, f_vals, label="Función original")
            plt.plot(x_vals, taylor_vals, label=f"Expansión de Taylor (n={terminos})", linestyle='--')
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title(f"Expansión en series de Taylor")
            plt.legend()
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", "Error al graficar la expansión")

# Algoritmos de optimización
class AlgoritmosOptimizacion(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self, text="Seleccionar algoritmo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algoritmo_var = tk.IntVar()
        algoritmos = [("Método de Gradiente", 1), ("Método de Newton", 2), ("Método de Conjugado Gradiente", 3)]
        for texto, valor in algoritmos:
            tk.Radiobutton(self, text=texto, variable=self.algoritmo_var, value=valor).grid(row=0, column=valor, padx=5, pady=5)

        tk.Label(self, text="Punto inicial (x, y):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_punto_inicial = tk.Entry(self, width=30)
        self.entrada_punto_inicial.insert(0, "(0, 0)")
        self.entrada_punto_inicial.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self, text="Número de iteraciones:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entrada_iteraciones = tk.Entry(self, width=10)
        self.entrada_iteraciones.insert(0, "100")
        self.entrada_iteraciones.grid(row=2, column=1, padx=5, pady=5)
        
        self.boton_ejecutar = tk.Button(self, text="Ejecutar", command=self.ejecutar_algoritmo)
        self.boton_ejecutar.grid(row=3, column=0, columnspan=2, pady=10)
        
    def ejecutar_algoritmo(self):
        try:
            algoritmo = self.algoritmo_var.get()
            punto_inicial = eval(self.entrada_punto_inicial.get())
            iteraciones = int(self.entrada_iteraciones.get())
            
            if algoritmo == 1:
                # Método de Gradiente
                pass
            elif algoritmo == 2:
                # Método de Newton
                pass
            elif algoritmo == 3:
                # Método de Conjugado Gradiente
                pass
            else:
                raise ValueError("Algoritmo no reconocido")
            
            # Aquí deberías implementar los métodos y mostrar los resultados
            # Según el algoritmo seleccionado
            pass
        
        except Exception as e:
            messagebox.showerror("Error", "Error al ejecutar el algoritmo")

# Aplicación principal
class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Optimización y Algoritmos")
        self.geometry("600x400")
        self.create_tabs()
        
    def create_tabs(self):
        tab_control = ttk.Notebook(self)
        
        tab1 = OptimizacionDosVariables(tab_control)
        tab2 = MatricesSparse(tab_control)
        tab3 = ExpansionTaylor(tab_control)
        tab4 = AlgoritmosOptimizacion(tab_control)
        
        tab_control.add(tab1, text="Optimización de Dos Variables")
        tab_control.add(tab2, text="Matrices Sparse")
        tab_control.add(tab3, text="Expansión en Series de Taylor")
        tab_control.add(tab4, text="Algoritmos de Optimización")
        
        tab_control.pack(expand=1, fill="both")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
