# Lab1-experimentos-con-problemas-de-optimización

Realizado por: Mariana Guerrero y Jonathan Castellanos.

Optimización 2184 

Septiembre 16,2024

------------------------------------------------------
El laboratorio contiene:
1. Un programa que grafica la región factible de una función dada. Modificando sus restricciones. 
2. Programa que convierte una matriz densa en dispersa, implementando el método de fila dispersa comprimida.
3. Un programa que permite observar la expansión de Taylor para 5 funciones, modificando el número de términos y el valor inicial X0.
4. Un programa para la optimización de 3 algoritmos sin restricción: Método de Newton, Método del Gradiente Descendente, y método BFGS. 

----------------------------------------------------
**Conclusiones Punto4:**

Los 3 algoritmos de optimización sin restricciones presentan resultados distintos. Para determinar el efecto que tiene cambiar sus parámetros es necesario analizar la tasa de aprendizaje, número de iteraciones y el punto inicial. 

En cuanto a la tasa de aprendizaje, escoger un valor de Alpha adecuado permitirá que se de una convergencia rápida y dará un equilibrio al algoritmo en el Gradiente Descendente. En  casos contrarios, un Alpha grande lo aleja de su convergencia, y un Alpha muy pequeño puede incurrir a un tiempo de convergencia lento. En los algoritmos utilizando método de Newton y BFGS no dependen de un valor de alpha, ya que, utilizan la información del gradiente y hessiano, sin embargo este último puede llegar a ser computacionalmente costoso en problemas de alta dimensión. 

Por otra parte, al cambiar el número de iteraciones, si es bajo es posible no alcanzar el punto óptimo. Es recomendable utilizar una cantidad alta para mejores resultados en Gradiente Descendente. Se debe tener en cuenta que el método de Newton y BFGS requieren menos iteraciones para alcanzar el mínimo, ya que suelen converger más rápido. Esto se puede evidenciar en la grafica del método BFGS, en el que solo aparece un punto en el plano, pues converge rápidamente la función y ha encontrado su mínimo. 

Finalmente, al realizar cambios en el punto inicial, los 3 algoritmos se ven afectados. Iniciar desde un punto cercano al mínimo hará que el algoritmo converja más rápido. En caso contrario, al tener un punto lejano, se necesita una cantidad mayor de iteraciones para alcanzar el mínimo global. 
