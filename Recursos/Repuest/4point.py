import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

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

# Configuración
x0 = np.array([5, 5])  # Punto inicial

# Parámetros
alpha = 0.1
num_iters = 50

# Resultados
grad_desc_history = gradient_descent(x0, alpha, num_iters)
newton_history = newton_method(x0, num_iters)
bfgs_history = bfgs_method(x0, num_iters)

# Graficar los resultados
plt.figure(figsize=(15, 5))

# Gradiente Descendente
plt.subplot(1, 3, 1)
plt.title("Gradiente Descendente")
plt.plot(grad_desc_history[:, 0], grad_desc_history[:, 1], 'o-')
plt.xlabel('x0')
plt.ylabel('x1')
plt.grid(True)

# Método de Newton
plt.subplot(1, 3, 2)
plt.title("Método de Newton")
plt.plot(newton_history[:, 0], newton_history[:, 1], 'o-')
plt.xlabel('x0')
plt.ylabel('x1')
plt.grid(True)

# Método BFGS
plt.subplot(1, 3, 3)
plt.title("Método BFGS")
plt.plot(bfgs_history[:, 0], bfgs_history[:, 1], 'o-')
plt.xlabel('x0')
plt.ylabel('x1')
plt.grid(True)

plt.tight_layout()
plt.show()
