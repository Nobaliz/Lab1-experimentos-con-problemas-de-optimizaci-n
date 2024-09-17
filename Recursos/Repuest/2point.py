import numpy as np
from scipy.sparse import csr_matrix

def csr_method(matrix):
  data = []
  ind_col = []
  indptr = [0]  # inicializa en 0
  nnz = 0  # contador elementos distintos de cero

  # iteración sobre filas
  for i in matrix:
    for j, val in enumerate(i): # encontrar cambio en columna
      if val != 0:
        data.append(val)
        ind_col.append(j)
        nnz += 1
    indptr.append(nnz)  # Número de elementos distintos de cero en la fila actual
  return np.array(data), np.array(ind_col), np.array(indptr)

def main():
  # matriz densa
  matriz_densa = np.array([[3, 0, 0, 7, 0, 0], [0, 0, 4, 0, 0, 1], [0, 0, 0, 3, 0, 0], [0, 0, 0, 7, 0, 1]])

  # resultados
  data, ind_col, indptr = csr_method(matriz_densa)
  print(' Matriz dispersa')
  print('Datos:', data)
  print('Índices columna:', ind_col)
  print('Cambio en fila:', indptr)

  # pasar matriz densa a CSR (scipy)
  matriz_sparse = csr_matrix(matriz_densa)
  print('\n Valores obtenidos de Scipy')
  print('CSR datos:', matriz_sparse.data)
  print('CSR indices columna:', matriz_sparse.indices)
  print('CSR cambio en fila:', matriz_sparse.indptr)

main()