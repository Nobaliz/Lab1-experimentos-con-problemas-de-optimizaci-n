import numpy as np
from scipy.sparse import csr_matrix
import tkinter as tk
from tkinter import messagebox

# Método CSR personalizado
def csr_method(matrix):
    data = []
    ind_col = []
    indptr = [0]  # Inicializa en 0
    nnz = 0  # Contador de elementos distintos de cero

    # Iteración sobre filas
    for i in matrix:
        for j, val in enumerate(i):  # Encontrar cambio en columna
            if val != 0:
                data.append(val)
                ind_col.append(j)
                nnz += 1
        indptr.append(nnz)  # Número de elementos distintos de cero en la fila actual
    return np.array(data), np.array(ind_col), np.array(indptr)

def simplify_data(data):
    return np.unique(data)  # Simplificar los datos mostrando solo valores únicos

def simplify_comparison(data, ind_col, indptr):
    simplified_data = simplify_data(data)
    simplified_ind_col = simplify_data(ind_col)
    simplified_indptr = simplify_data(indptr)
    return simplified_data, simplified_ind_col, simplified_indptr

def process_matrix():
    try:
        # Obtener los valores de las entradas
        rows = int(rows_entry.get())
        cols = int(cols_entry.get())
        min_val = int(min_val_entry.get())
        max_val = int(max_val_entry.get())
        sparsity = float(sparsity_entry.get())

        # Generar la matriz dispersa
        matrix = generate_sparse_matrix(rows, cols, min_val, max_val, sparsity)

        # Mostrar la matriz dispersa en el cuadro de texto
        matrix_display.config(state=tk.NORMAL)
        matrix_display.delete("1.0", tk.END)
        for row in matrix:
            matrix_display.insert(tk.END, ' '.join(f'{val}' for val in row) + '\n')
        matrix_display.config(state=tk.DISABLED)

        # Calcular CSR manualmente
        data, ind_col, indptr = csr_method(matrix)
        csr_manual = f'Datos: {np.array2string(data, separator=", ", threshold=np.inf)}\n' \
                     f'Índices columna: {np.array2string(ind_col, separator=", ", threshold=np.inf)}\n' \
                     f'Cambios de fila: {np.array2string(indptr, separator=", ", threshold=np.inf)}'

        # Calcular CSR usando scipy
        csr_scipy = csr_matrix(matrix)
        csr_scipy_result = f'Datos: {np.array2string(csr_scipy.data, separator=", ", threshold=np.inf)}\n' \
                           f'Índices columna: {np.array2string(csr_scipy.indices, separator=", ", threshold=np.inf)}\n' \
                           f'Cambios de fila: {np.array2string(csr_scipy.indptr, separator=", ", threshold=np.inf)}'

        # Mostrar resultados en los cuadros de texto de comparación
        csr_manual_display.config(state=tk.NORMAL)
        csr_manual_display.delete("1.0", tk.END)
        csr_manual_display.insert(tk.END, csr_manual)
        csr_manual_display.config(state=tk.DISABLED)

        csr_scipy_display.config(state=tk.NORMAL)
        csr_scipy_display.delete("1.0", tk.END)
        csr_scipy_display.insert(tk.END, csr_scipy_result)
        csr_scipy_display.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Asegúrate de ingresar valores válidos.")

def simplify_comparisons():
    try:
        # Extraer datos de los cuadros de texto
        matrix_str = matrix_display.get("1.0", tk.END).strip()
        matrix = np.array([[int(num) for num in row.split()] for row in matrix_str.split('\n')])

        # Calcular CSR manualmente
        data, ind_col, indptr = csr_method(matrix)
        simplified_data, simplified_ind_col, simplified_indptr = simplify_comparison(data, ind_col, indptr)

        # Mostrar datos simplificados en el cuadro de comparación manual
        simplified_csr_manual = f'Datos simplificados: {np.array2string(simplified_data, separator=", ", threshold=np.inf)}\n' \
                                f'Índices columna simplificados: {np.array2string(simplified_ind_col, separator=", ", threshold=np.inf)}\n' \
                                f'Cambios de fila simplificados: {np.array2string(simplified_indptr, separator=", ", threshold=np.inf)}'
        csr_manual_display.config(state=tk.NORMAL)
        csr_manual_display.delete("1.0", tk.END)
        csr_manual_display.insert(tk.END, simplified_csr_manual)
        csr_manual_display.config(state=tk.DISABLED)

        # Simplificar datos de SciPy
        csr_scipy = csr_matrix(matrix)
        simplified_scipy_data, simplified_scipy_ind_col, simplified_scipy_indptr = simplify_comparison(
            csr_scipy.data, csr_scipy.indices, csr_scipy.indptr)

        simplified_csr_scipy = f'Datos simplificados: {np.array2string(simplified_scipy_data, separator=", ", threshold=np.inf)}\n' \
                               f'Índices columna simplificados: {np.array2string(simplified_scipy_ind_col, separator=", ", threshold=np.inf)}\n' \
                               f'Cambios de fila simplificados: {np.array2string(simplified_scipy_indptr, separator=", ", threshold=np.inf)}'
        csr_scipy_display.config(state=tk.NORMAL)
        csr_scipy_display.delete("1.0", tk.END)
        csr_scipy_display.insert(tk.END, simplified_csr_scipy)
        csr_scipy_display.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Error al simplificar los datos.")

def generate_sparse_matrix(rows, cols, min_val, max_val, sparsity):
    matrix = np.zeros((rows, cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            if np.random.rand() > sparsity:  # Genera ceros según la proporción
                matrix[i][j] = np.random.randint(min_val, max_val + 1)
    return matrix

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Generador de Matrices Dispersas y Comparación CSR")
root.config(bg="#481F67")
root.resizable(False, False)  # Deshabilitar redimensionamiento

# Frame para las entradas
frame_inputs = tk.Frame(root, bg="#481F67")
frame_inputs.pack(padx=10, pady=10)

tk.Label(frame_inputs, text="Filas:", bg="#481F67", fg="white").grid(row=0, column=0)
rows_entry = tk.Entry(frame_inputs, bg="#321244", fg="white")
rows_entry.grid(row=0, column=1)

tk.Label(frame_inputs, text="Columnas:", bg="#481F67", fg="white").grid(row=1, column=0)
cols_entry = tk.Entry(frame_inputs, bg="#321244", fg="white")
cols_entry.grid(row=1, column=1)

tk.Label(frame_inputs, text="Valor mínimo:", bg="#481F67", fg="white").grid(row=2, column=0)
min_val_entry = tk.Entry(frame_inputs, bg="#321244", fg="white")
min_val_entry.grid(row=2, column=1)

tk.Label(frame_inputs, text="Valor máximo:", bg="#481F67", fg="white").grid(row=3, column=0)
max_val_entry = tk.Entry(frame_inputs, bg="#321244", fg="white")
max_val_entry.grid(row=3, column=1)

tk.Label(frame_inputs, text="Proporción de ceros (0 a 1):", bg="#481F67", fg="white").grid(row=4, column=0)
sparsity_entry = tk.Entry(frame_inputs, bg="#321244", fg="white")
sparsity_entry.grid(row=4, column=1)

process_button = tk.Button(frame_inputs, text="Generar Matriz", command=process_matrix, bg="#5A2D77", fg="white")
process_button.grid(row=5, column=0, columnspan=2, pady=10)

simplify_button = tk.Button(frame_inputs, text="Simplificar Datos", command=simplify_comparisons, bg="#5A2D77", fg="white")
simplify_button.grid(row=6, column=0, columnspan=2, pady=10)

# Frame para la matriz generada
frame_matrix = tk.Frame(root, bg="#481F67")
frame_matrix.pack(padx=10, pady=10)

matrix_display = tk.Text(frame_matrix, height=10, width=60, bg="#321244", fg="white", wrap=tk.NONE)
matrix_display.grid(row=0, column=0, sticky="nsew")
matrix_scroll_x = tk.Scrollbar(frame_matrix, orient="horizontal", command=matrix_display.xview)
matrix_scroll_x.grid(row=1, column=0, sticky="ew")
matrix_display.config(xscrollcommand=matrix_scroll_x.set)
matrix_display.config(state=tk.DISABLED)

# Frame para la comparación CSR
frame_comparison = tk.Frame(root, bg="#481F67")
frame_comparison.pack(padx=10, pady=10)

tk.Label(frame_comparison, text="CSR Manual", bg="#481F67", fg="white").grid(row=0, column=0)
csr_manual_display = tk.Text(frame_comparison, height=10, width=60, bg="#321244", fg="white", wrap=tk.NONE)
csr_manual_display.grid(row=1, column=0, sticky="nsew")
csr_manual_display.config(state=tk.DISABLED)

tk.Label(frame_comparison, text="CSR SciPy", bg="#481F67", fg="white").grid(row=0, column=1)
csr_scipy_display = tk.Text(frame_comparison, height=10, width=60, bg="#321244", fg="white", wrap=tk.NONE)
csr_scipy_display.grid(row=1, column=1, sticky="nsew")
csr_scipy_display.config(state=tk.DISABLED)

root.mainloop()
