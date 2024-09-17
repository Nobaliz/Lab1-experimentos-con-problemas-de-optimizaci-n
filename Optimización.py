import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

class LPModelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelo de Programación Lineal")
        self.geometry("350x450")
        self.configure(bg="#481F67")  # Color de fondo principal
        self.resizable(0,0)
        # Colores de texto, fondo y entrada de texto
        bg_color = "#481F67"
        fg_color = "#FFFFFF"
        entry_bg_color = "#321244"

        # Frame superior para variables de decisión
        frame_vars = tk.Frame(self, bg=bg_color, padx=10, pady=10)
        frame_vars.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.label_var_x = tk.Label(frame_vars, text="Nombre de X:", bg=bg_color, fg=fg_color)
        self.label_var_x.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_var_x = tk.Entry(frame_vars, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        self.entry_var_x.grid(row=0, column=1, padx=5, pady=5)

        self.label_var_y = tk.Label(frame_vars, text="Nombre de Y:", bg=bg_color, fg=fg_color)
        self.label_var_y.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_var_y = tk.Entry(frame_vars, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        self.entry_var_y.grid(row=1, column=1, padx=5, pady=5)

        # Frame para elementos de la tabla
        frame_table = tk.Frame(self, bg=bg_color, padx=10, pady=10)
        frame_table.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.label_elementos = tk.Label(frame_table, text="Elementos:", bg=bg_color, fg=fg_color)
        self.label_elementos.grid(row=0, column=0, padx=5, pady=5)
        self.label_x = tk.Label(frame_table, text="X:", bg=bg_color, fg=fg_color)
        self.label_x.grid(row=0, column=1, padx=5, pady=5)
        self.label_y = tk.Label(frame_table, text="Y:", bg=bg_color, fg=fg_color)
        self.label_y.grid(row=0, column=2, padx=5, pady=5)
        self.label_limite = tk.Label(frame_table, text="Límite (<=):", bg=bg_color, fg=fg_color)
        self.label_limite.grid(row=0, column=3, padx=5, pady=5)

        self.create_element_row(frame_table, "Elem_1:", 1, bg_color, fg_color, entry_bg_color)
        self.create_element_row(frame_table, "Elem_2:", 2, bg_color, fg_color, entry_bg_color)
        self.create_element_row(frame_table, "Elem_3:", 3, bg_color, fg_color, entry_bg_color)

        # Frame para unit profit
        frame_profit = tk.Frame(self, bg=bg_color, padx=10, pady=10)
        frame_profit.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.label_profit = tk.Label(frame_profit, text="Unit Profit (X, Y):", bg=bg_color, fg=fg_color)
        self.label_profit.grid(row=0, column=0, padx=5, pady=5)
        
        self.entry_profit_x = tk.Entry(frame_profit, width=10, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        self.entry_profit_x.grid(row=0, column=1, padx=5, pady=5)
        self.entry_profit_y = tk.Entry(frame_profit, width=10, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        self.entry_profit_y.grid(row=0, column=2, padx=5, pady=5)

        # Botón para generar el modelo LP
        frame_buttons = tk.Frame(self, bg=bg_color, padx=10, pady=10)
        frame_buttons.grid(row=3, column=0, padx=10, pady=10)

        self.btn_generate = tk.Button(frame_buttons, text="Generar Modelo",bg="#481F67",fg="#FFFFFF", command=self.generar_modelo)
        self.btn_generate.grid(row=0, column=0, padx=10, pady=10)

    def create_element_row(self, frame, label_text, row, bg_color, fg_color, entry_bg_color):
        label = tk.Label(frame, text=label_text, bg=bg_color, fg=fg_color)
        label.grid(row=row, column=0, padx=5, pady=5)
        
        entry_x = tk.Entry(frame, width=10, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        entry_x.grid(row=row, column=1, padx=5, pady=5)
        entry_y = tk.Entry(frame, width=10, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        entry_y.grid(row=row, column=2, padx=5, pady=5)
        entry_limit = tk.Entry(frame, width=10, bg=entry_bg_color, fg=fg_color, insertbackground=fg_color)
        entry_limit.grid(row=row, column=3, padx=5, pady=5)

        setattr(self, f"entry_elem{row}_x", entry_x)
        setattr(self, f"entry_elem{row}_y", entry_y)
        setattr(self, f"entry_elem{row}_limit", entry_limit)

    def generar_modelo(self):
        var_x = self.entry_var_x.get()
        var_y = self.entry_var_y.get()

        profit_x = float(self.entry_profit_x.get())
        profit_y = float(self.entry_profit_y.get())
        funcion_objetivo = f"Maximizar Z = {profit_x}*{var_x} + {profit_y}*{var_y}"

        restriccion_1 = f"{self.entry_elem1_x.get()}*{var_x} + {self.entry_elem1_y.get()}*{var_y} <= {self.entry_elem1_limit.get()}"
        restriccion_2 = f"{self.entry_elem2_x.get()}*{var_x} + {self.entry_elem2_y.get()}*{var_y} <= {self.entry_elem2_limit.get()}"
        restriccion_3 = f"{self.entry_elem3_x.get()}*{var_x} + {self.entry_elem3_y.get()}*{var_y} <= {self.entry_elem3_limit.get()}"

        restricciones_no_negativas = f"{var_x} >= 0, {var_y} >= 0"

        model_window = tk.Toplevel(self)
        model_window.title("Modelo LP")
        model_window.geometry("400x300")
        model_window.configure(bg="#481F67")

        tk.Label(model_window, text="1. Definición de las variables de decisión:", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {var_x}: {var_x}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {var_y}: {var_y}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")

        tk.Label(model_window, text="2. Función Objetivo:", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {funcion_objetivo}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")

        tk.Label(model_window, text="3. Restricciones:", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {restriccion_1}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {restriccion_2}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {restriccion_3}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")

        tk.Label(model_window, text="4. Restricciones No Negativas:", bg="#481F67", fg="#FFFFFF").pack(anchor="w")
        tk.Label(model_window, text=f"   {restricciones_no_negativas}", bg="#481F67", fg="#FFFFFF").pack(anchor="w")

        tk.Button(model_window, text="Graficar",bg="#481F67",fg="#FFFFFF" ,command=self.graficar).pack(pady=10)

    def graficar(self):
        try:
            x = np.linspace(0, 300, 300)

            y1 = ((float(self.entry_elem1_limit.get()) - float(self.entry_elem1_x.get()) * x)) / float(self.entry_elem1_y.get())
            y2 = ((float(self.entry_elem2_limit.get()) - float(self.entry_elem2_x.get()) * x)) / float(self.entry_elem2_y.get())
            y3 = ((float(self.entry_elem3_limit.get()) - float(self.entry_elem3_x.get()) * x)) / float(self.entry_elem3_y.get())

            plt.plot(x, y1, label="Restricción 1")
            plt.plot(x, y2, label="Restricción 2")
            plt.plot(x, y3, label="Restricción 3")

            plt.fill_between(x, 0, y1, where=(y1 >= 0), color='gray', alpha=0.5)
            plt.fill_between(x, 0, y2, where=(y2 >= 0), color='gray', alpha=0.5)
            plt.fill_between(x, 0, y3, where=(y3 >= 0), color='gray', alpha=0.5)

            plt.xlim((0, 300))
            plt.ylim((0, 300))

            plt.xlabel(self.entry_var_x.get())
            plt.ylabel(self.entry_var_y.get())

            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al graficar: {e}")

if __name__ == "__main__":
    app = LPModelApp()
    app.mainloop()
