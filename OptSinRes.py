import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import tkinter as tk
from tkinter import ttk

# Definimos una función de ejemplo
def objective_function(x):
    return x[0]**2 + x[1]**2  # Función cuadrática simple

# Gradiente de la función
def gradient(x):
    return np.array([2*x[0], 2*x[1]])

# Hessiana de la función
def hessian(x):
    return np.array([[2, 0], [0, 2]])

# Algoritmos
def gradient_descent(x0, alpha=0.01, num_iters=100):
    x = x0
    history = [x0]
    for _ in range(num_iters):
        grad = gradient(x)
        x = x - alpha * grad
        history.append(x)
    return np.array(history)

def newton_method(x0, num_iters=100):
    x = x0
    history = [x0]
    for _ in range(num_iters):
        grad = gradient(x)
        H = hessian(x)
        x = x - np.linalg.inv(H).dot(grad)
        history.append(x)
    return np.array(history)

def bfgs_method(x0, num_iters=100):
    res = minimize(objective_function, x0, method='BFGS', jac=gradient, options={'maxiter': num_iters})
    return np.array([res.x for _ in range(num_iters+1)])  # Resuelve una sola vez, para comparación

# Función para mostrar gráficos en una ventana separada
def show_graphs():
    # Obtener parámetros de la interfaz gráfica
    x0 = np.array([float(x0_x_entry.get()), float(x0_y_entry.get())])
    alpha = float(alpha_entry.get())
    num_iters = int(num_iters_entry.get())
    
    # Ejecutar algoritmos
    grad_desc_history = gradient_descent(x0, alpha, num_iters)
    newton_history = newton_method(x0, num_iters)
    bfgs_history = bfgs_method(x0, num_iters)

    # Crear gráficos
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].plot(grad_desc_history[:, 0], grad_desc_history[:, 1], 'o-')
    axs[0].set_title("Gradiente Descendente")
    axs[0].set_xlabel('x0')
    axs[0].set_ylabel('x1')
    axs[0].grid(True)

    axs[1].plot(newton_history[:, 0], newton_history[:, 1], 'o-')
    axs[1].set_title("Método de Newton")
    axs[1].set_xlabel('x0')
    axs[1].set_ylabel('x1')
    axs[1].grid(True)

    axs[2].plot(bfgs_history[:, 0], bfgs_history[:, 1], 'o-')
    axs[2].set_title("Método BFGS")
    axs[2].set_xlabel('x0')
    axs[2].set_ylabel('x1')
    axs[2].grid(True)

    plt.tight_layout()
    
    # Mostrar los gráficos en una nueva ventana
    plt.show()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Optimización de Algoritmos")
root.config(bg="#481F67")
# Frame para los controles
control_frame = tk.Frame(root,bg="#7030A0")
control_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Parámetros de entrada
tk.Label(control_frame, text="Punto Inicial x:",bg="#7030A0",fg="white").grid(row=0, column=0, sticky=tk.W)
x0_x_entry = tk.Entry(control_frame,bg="#321244", fg="white")
x0_x_entry.grid(row=0, column=1)
x0_x_entry.insert(0, '5')

tk.Label(control_frame, text="Punto Inicial y:",bg="#7030A0",fg="white").grid(row=1, column=0, sticky=tk.W)
x0_y_entry = tk.Entry(control_frame,bg="#321244", fg="white")
x0_y_entry.grid(row=1, column=1)
x0_y_entry.insert(0, '5')

tk.Label(control_frame, text="Tasa de Aprendizaje (Alpha):",bg="#7030A0",fg="white").grid(row=2, column=0, sticky=tk.W)
alpha_entry = tk.Entry(control_frame,bg="#321244", fg="white")
alpha_entry.grid(row=2, column=1)
alpha_entry.insert(0, '0.1')

tk.Label(control_frame, text="Número de Iteraciones:",bg="#7030A0",fg="white").grid(row=3, column=0, sticky=tk.W)
num_iters_entry = tk.Entry(control_frame,bg="#321244", fg="white")
num_iters_entry.grid(row=3, column=1)
num_iters_entry.insert(0, '50')

# Botón para mostrar gráficos
show_button = tk.Button(control_frame, text="Mostrar Gráficos",bg="#321244", fg="white", command=show_graphs)
show_button.grid(row=4, columnspan=2, pady=10)

root.mainloop()
