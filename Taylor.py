import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Expansión en series de Taylor
def taylor_expansion(func, x0, n):
    x = sp.symbols('x')
    taylor_series = sum((func.diff(x, k).subs(x, x0) * (x - x0)**k) / sp.factorial(k) for k in range(n + 1))
    return taylor_series

# Funciones disponibles
def func_selector(opcion):
    x = sp.symbols('x')
    if opcion == 1:
        return sp.sin(x)  # seno
    elif opcion == 2:
        return x**2 + 3*x + 2  # función polinómica grado 2
    elif opcion == 3:
        return sp.exp(x)  # exponencial
    elif opcion == 4:
        return sp.log(1 + x)  # logaritmo natural
    elif opcion == 5:
        return 1/x  # función recíproca
    else:
        return None

def plot_function(func, taylor, x0, n):
    x = sp.symbols('x')
    
    # Determinar el rango de x
    if func == sp.log(1 + x):  # log(1 + x)
        x_values = np.linspace(-0.9, 5, 1000)  # rango limitado para evitar x <= -1
    elif func == 1/x:  # 1/x
        x_values = np.linspace(0.1, 10, 1000)  # solo para evitar división por cero
    else:
        x_values = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
    
    func_taylor = sp.lambdify(x, taylor, 'numpy')
    f_original = sp.lambdify(x, func, 'numpy')

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, f_original(x_values), label='Función original', color='blue')
    plt.plot(x_values, func_taylor(x_values), label=f'Serie de Taylor (n={n})', color='red')
    plt.legend()
    plt.title('Gráfica de la función y su serie de Taylor')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.show()

def on_plot_button_click():
    try:
        opcion = func_var.get()
        n = int(n_terms_entry.get())
        x0 = float(x0_entry.get())

        func = func_selector(opcion)
        if func is None:
            raise ValueError("Opción no válida")

        taylor = taylor_expansion(func, x0, n)
        plot_function(func, taylor, x0, n)

    except ValueError as e:
        messagebox.showerror("Error", f"Entrada no válida: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Expansión en Series de Taylor")
root.config(bg="#481F67")
root.resizable(0,0)
# Frame para selección de función
frame_func = tk.Frame(root, bg="#481F67")
frame_func.pack(padx=10, pady=10)

tk.Label(frame_func, text="Selecciona la función:", bg="#481F67", fg="white").grid(row=0, column=0, sticky=tk.W)

func_var = tk.IntVar()

# Personalización de los Radiobutton
radio_style = {'bg': "#481F67", 'fg': "white", 'selectcolor': "#B55B95"}

tk.Radiobutton(frame_func, text='sin(x)', variable=func_var, value=1, **radio_style).grid(row=1, column=0, sticky=tk.W)
tk.Radiobutton(frame_func, text='x^2 + 3x + 2', variable=func_var, value=2, **radio_style).grid(row=2, column=0, sticky=tk.W)
tk.Radiobutton(frame_func, text='exp(x)', variable=func_var, value=3, **radio_style).grid(row=3, column=0, sticky=tk.W)
tk.Radiobutton(frame_func, text='log(1 + x)', variable=func_var, value=4, **radio_style).grid(row=4, column=0, sticky=tk.W)
tk.Radiobutton(frame_func, text='1/x', variable=func_var, value=5, **radio_style).grid(row=5, column=0, sticky=tk.W)

# Frame para entrada de datos
frame_data = tk.Frame(root, bg="#481F67")
frame_data.pack(padx=10, pady=10)

tk.Label(frame_data, text="Número de términos:", bg="#481F67", fg="white").grid(row=0, column=0, sticky=tk.W)
n_terms_entry = tk.Entry(frame_data)
n_terms_entry.grid(row=0, column=1)

tk.Label(frame_data, text="Punto de expansión x0:", bg="#481F67", fg="white").grid(row=1, column=0, sticky=tk.W)
x0_entry = tk.Entry(frame_data)
x0_entry.grid(row=1, column=1)

plot_button = tk.Button(root, text="Graficar", command=on_plot_button_click, bg="#321244", fg="white")
plot_button.pack(pady=10)

root.mainloop()
