import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import tkinter as tk
from tkinter import ttk
import time

# Evaluar la función proporcionada por el usuario
def evaluate_function(x):
    try:
        # Convierte la cadena de la función en una expresión evaluable
        return eval(function_entry.get(), {"x": x, "np": np})
    except Exception as e:
        print(f"Error al evaluar la función: {e}")
        return np.inf

# Gradiente de la función usando diferencias finitas
def gradient(x):
    eps = 1e-6
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x1 = np.copy(x)
        x1[i] += eps
        grad[i] = (evaluate_function(x1) - evaluate_function(x)) / eps
    return grad

# Hessiana de la función usando diferencias finitas
def hessian(x):
    eps = 1e-6
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x1 = np.copy(x)
            if i == j:
                x1[i] += eps
                H[i, j] = (evaluate_function(x1) - evaluate_function(x)) / eps
            else:
                x1[i] += eps
                x1[j] += eps
                f1 = evaluate_function(x1)
                x1[j] -= 2 * eps
                f2 = evaluate_function(x1)
                x1[i] -= 2 * eps
                f3 = evaluate_function(x1)
                x1[j] += 2 * eps
                f4 = evaluate_function(x1)
                H[i, j] = (f1 - f2 - f3 + f4) / (4 * eps ** 2)
    return H

# Algoritmos
def gradient_descent(x0, alpha=0.01, num_iters=100):
    x = np.copy(x0)
    history = [x0]
    start_time = time.time()
    for _ in range(num_iters):
        grad = gradient(x)
        x = x - alpha * grad
        history.append(np.copy(x))
    elapsed_time = time.time() - start_time
    return np.array(history), elapsed_time

def newton_method(x0, num_iters=100):
    x = np.copy(x0)
    history = [x0]
    start_time = time.time()
    for _ in range(num_iters):
        grad = gradient(x)
        H = hessian(x)
        if np.linalg.cond(H) < 1 / np.finfo(H.dtype).eps:  # Verificar si la Hessiana es invertible
            x = x - np.linalg.inv(H).dot(grad)
            history.append(np.copy(x))
        else:
            print("La Hessiana no es invertible.")
            break
    elapsed_time = time.time() - start_time
    return np.array(history), elapsed_time

def bfgs_method(x0, num_iters=100):
    start_time = time.time()
    history = [x0]
    
    def callback(xk):
        history.append(np.copy(xk))
    
    res = minimize(evaluate_function, x0, method='BFGS', jac=gradient, callback=callback, options={'maxiter': num_iters})
    elapsed_time = time.time() - start_time
    return np.array(history), elapsed_time

# Función para mostrar gráficos en una ventana separada
def show_graphs():
    # Obtener parámetros de la interfaz gráfica
    x0 = np.array([float(x0_x_entry.get()), float(x0_y_entry.get())])
    alpha = float(alpha_entry.get())
    num_iters = int(num_iters_entry.get())
    min_range = float(min_entry.get())
    max_range = float(max_entry.get())
    
    # Ejecutar algoritmos
    grad_desc_history, grad_desc_time = gradient_descent(x0, alpha, num_iters)
    newton_history, newton_time = newton_method(x0, num_iters)
    bfgs_history, bfgs_time = bfgs_method(x0, num_iters)

    # Crear una cuadrícula para el espacio de la función
    x = np.linspace(min_range, max_range, 400)
    y = np.linspace(min_range, max_range, 400)
    X, Y = np.meshgrid(x, y)
    Z = np.array([evaluate_function(np.array([xi, yi])) for xi, yi in zip(np.ravel(X), np.ravel(Y))])
    Z = Z.reshape(X.shape)

    # Crear gráficos
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Gradiente Descendente
    axs[0].contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.5)
    axs[0].plot(grad_desc_history[:, 0], grad_desc_history[:, 1], 'o-', color='r', label='Trayectoria')
    axs[0].set_title(f"Gradiente Descendente\nTiempo: {grad_desc_time:.4f} s\nIteraciones: {len(grad_desc_history)-1}")
    axs[0].set_xlabel('x0')
    axs[0].set_ylabel('x1')
    axs[0].grid(True)
    axs[0].set_xlim([min_range, max_range])
    axs[0].set_ylim([min_range, max_range])
    axs[0].legend()

    # Método de Newton
    axs[1].contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.5)
    if newton_history.size > 0:
        axs[1].plot(newton_history[:, 0], newton_history[:, 1], 'o-', color='g', label='Trayectoria')
    axs[1].set_title(f"Método de Newton\nTiempo: {newton_time:.4f} s\nIteraciones: {len(newton_history)-1}")
    axs[1].set_xlabel('x0')
    axs[1].set_ylabel('x1')
    axs[1].grid(True)
    axs[1].set_xlim([min_range, max_range])
    axs[1].set_ylim([min_range, max_range])
    axs[1].legend()

    # Método BFGS
    axs[2].contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.5)
    if bfgs_history.size > 0:
        axs[2].plot(bfgs_history[:, 0], bfgs_history[:, 1], 'o-', color='b', label='Trayectoria')
    axs[2].set_title(f"Método BFGS\nTiempo: {bfgs_time:.4f} s\nIteraciones: {len(bfgs_history)-1}")
    axs[2].set_xlabel('x0')
    axs[2].set_ylabel('x1')
    axs[2].grid(True)
    axs[2].set_xlim([min_range, max_range])
    axs[2].set_ylim([min_range, max_range])
    axs[2].legend()

    plt.tight_layout()
    plt.show()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Optimización de Algoritmos")
root.config(bg="#481F67")
root.resizable(0,0)

# Frame para los controles
control_frame = tk.Frame(root, bg="#7030A0")
control_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Parámetros de entrada
tk.Label(control_frame, text="Punto Inicial x:", bg="#7030A0", fg="white").grid(row=0, column=0, sticky=tk.W)
x0_x_entry = tk.Entry(control_frame, bg="#321244", fg="white")
x0_x_entry.grid(row=0, column=1)
x0_x_entry.insert(0, '5')

tk.Label(control_frame, text="Punto Inicial y:", bg="#7030A0", fg="white").grid(row=1, column=0, sticky=tk.W)
x0_y_entry = tk.Entry(control_frame, bg="#321244", fg="white")
x0_y_entry.grid(row=1, column=1)
x0_y_entry.insert(0, '5')

tk.Label(control_frame, text="Función (use 'x[0]' y 'x[1]'):", bg="#7030A0", fg="white").grid(row=2, column=0, sticky=tk.W)
function_entry = tk.Entry(control_frame, bg="#321244", fg="white")
function_entry.grid(row=2, column=1)
function_entry.insert(0, 'x[0]**2 + x[1]**2')

tk.Label(control_frame, text="Tasa de Aprendizaje (Alpha):", bg="#7030A0", fg="white").grid(row=3, column=0, sticky=tk.W)
alpha_entry = tk.Entry(control_frame, bg="#321244", fg="white")
alpha_entry.grid(row=3, column=1)
alpha_entry.insert(0, '0.1')

tk.Label(control_frame, text="Número de Iteraciones:", bg="#7030A0", fg="white").grid(row=4, column=0, sticky=tk.W)
num_iters_entry = tk.Entry(control_frame, bg="#321244", fg="white")
num_iters_entry.grid(row=4, column=1)
num_iters_entry.insert(0, '50')

tk.Label(control_frame, text="Rango Mínimo:", bg="#7030A0", fg="white").grid(row=5, column=0, sticky=tk.W)
min_entry = tk.Entry(control_frame, bg="#321244", fg="white")
min_entry.grid(row=5, column=1)
min_entry.insert(0, '-5')

tk.Label(control_frame, text="Rango Máximo:", bg="#7030A0", fg="white").grid(row=6, column=0, sticky=tk.W)
max_entry = tk.Entry(control_frame, bg="#321244", fg="white")
max_entry.grid(row=6, column=1)
max_entry.insert(0, '5')

# Botón para mostrar gráficos
show_button = tk.Button(control_frame, text="Mostrar Gráficos", bg="#321244", fg="white", command=show_graphs)
show_button.grid(row=7, columnspan=2, pady=10)

root.mainloop()
