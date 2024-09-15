
import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Aplicacion(tk.Tk):    
    def __init__(self):
        super().__init__()
        self.config(bg="#481F67")
        self.title("Optimización Gráfica")
        self.geometry("235x400")
        
        #frames
        self.frame_funcion = tk.Frame(self,bg="#7030A0")
        self.frame_funcion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.frame_restriccion = tk.Frame(self,bg="#7030A0")
        self.frame_restriccion.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.frame_valores = tk.Frame(self,bg="#7030A0")
        self.frame_valores.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Frame 1: Función de costo
        self.etiqueta_funcion = tk.Label(self.frame_funcion, text="Función de costo:",bg="#7030A0",fg="white")
        self.etiqueta_funcion.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entrada_funcion = tk.Entry(self.frame_funcion, width=15,bg="#321244", fg="white")
        self.entrada_funcion.insert(0,"x+y")
        self.entrada_funcion.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_funcion.bind("<KeyRelease>", self.calcular_funcion_costo)
        
        # Frame 2: Restricción y gráfica
        self.etiqueta_restriccion = tk.Label(self.frame_restriccion, text="Restricción (x + y ≤ ):",bg="#7030A0",fg="white")
        self.etiqueta_restriccion.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entrada_restriccion = tk.Entry(self.frame_restriccion, width=10,bg="#321244", fg="white")
        self.entrada_restriccion.grid(row=0, column=1, padx=5, pady=5)
        
        self.etiqueta_x_min = tk.Label(self.frame_restriccion, text="Escala X (min):",bg="#7030A0",fg="white")
        self.etiqueta_x_min.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.escala_x_min = tk.Entry(self.frame_restriccion, width=5,bg="#321244", fg="white")
        self.escala_x_min.insert(0, "0")
        self.escala_x_min.grid(row=1, column=1, padx=5, pady=5)
        
        self.etiqueta_x_max = tk.Label(self.frame_restriccion, text="Escala X (max):",bg="#7030A0",fg="white")
        self.etiqueta_x_max.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.escala_x_max = tk.Entry(self.frame_restriccion, width=5,bg="#321244", fg="white")
        self.escala_x_max.insert(0, "5")
        self.escala_x_max.grid(row=2, column=1, padx=5, pady=5)
        
        self.etiqueta_y_min = tk.Label(self.frame_restriccion, text="Escala Y (min):",bg="#7030A0",fg="white")
        self.etiqueta_y_min.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.escala_y_min = tk.Entry(self.frame_restriccion, width=5,bg="#321244", fg="white")
        self.escala_y_min.insert(0, "0")
        self.escala_y_min.grid(row=3, column=1, padx=5, pady=5)
        
        self.etiqueta_y_max = tk.Label(self.frame_restriccion, text="Escala Y (max):",bg="#7030A0",fg="white")
        self.etiqueta_y_max.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.escala_y_max = tk.Entry(self.frame_restriccion, width=5,bg="#321244", fg="white")
        self.escala_y_max.insert(0, "5")
        self.escala_y_max.grid(row=4, column=1, padx=5, pady=5)
        
        self.boton_graficar = tk.Button(self.frame_restriccion, text="Graficar", command=self.graficar_region_factible,bg="#481F67",fg="white")
        self.boton_graficar.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Frame 3: Valores de X y Y
        self.etiqueta_x = tk.Label(self.frame_valores, text="Valor de X:",bg="#7030A0",fg="white")
        self.etiqueta_x.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entrada_x = tk.Entry(self.frame_valores, width=10,bg="#321244", fg="white")
        self.entrada_x.insert(0, "0")
        self.entrada_x.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_x.bind("<KeyRelease>", self.calcular_funcion_costo)
        
        self.etiqueta_y = tk.Label(self.frame_valores, text="Valor de Y:",bg="#7030A0",fg="white")
        self.etiqueta_y.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.entrada_y = tk.Entry(self.frame_valores, width=10,bg="#321244", fg="white")
        self.entrada_y.insert(0, "0")
        self.entrada_y.grid(row=1, column=1, padx=5, pady=5)
        self.entrada_y.bind("<KeyRelease>", self.calcular_funcion_costo)
        
        self.etiqueta_resultado = tk.Label(self, text="Resultado: ",bg="#481F67",fg="white")
        self.etiqueta_resultado.grid(row=3, column=0, padx=10, pady=10)
        
        self.calcular_funcion_costo()
    
    def calcular_funcion_costo(self, event=None):
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

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
