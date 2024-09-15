import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import numpy 
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optigraph")  # Cambiar el título de la ventana
        self.geometry("400x250")
        
        # Fondo
        bg_image = Image.open("Recursos/Fondo.png")
        bg_image = bg_image.resize((400, 250), Image.LANCZOS)  # Redimensiona la imagen al tamaño de la ventana
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        background_label = tk.Label(self, image=self.bg_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Crear el título en la parte superior, centrado
        self.titulo = tk.Label(self, text=" 𝕆𝕡𝕥𝕚𝔾𝕣𝕒𝕡𝕙", font=("Eras Demi ITC", 40),bg="#481F67",fg="#FFFFFF")   
        
        self.titulo.pack(pady=20,anchor='w')# Agregar separación con pady

        # Frame para los botones
        self.frame_botones = tk.Frame(self,bg="#481F67")
        self.frame_botones.pack(pady=10)

        # Cargar imágenes y crear botones para cada algoritmo
        self.img_opt = ImageTk.PhotoImage(Image.open("Recursos/Optimización.png").resize((60, 60)))
        self.img_sparse = ImageTk.PhotoImage(Image.open("Recursos/Sparce.png").resize((60, 60)))
        self.img_taylor = ImageTk.PhotoImage(Image.open("Recursos/Taylor.png").resize((60, 60)))
        self.img_algos = ImageTk.PhotoImage(Image.open("Recursos/AlSinRe.png").resize((60, 60)))

        self.boton_opt = tk.Button(self.frame_botones, image=self.img_opt, command=self.ejecutar_optimizacion)
        self.boton_opt.grid(row=0, column=0, padx=10, pady=10)

        self.boton_sparse = tk.Button(self.frame_botones, image=self.img_sparse, command=self.ejecutar_sparse)
        self.boton_sparse.grid(row=0, column=1, padx=10, pady=10)

        self.boton_taylor = tk.Button(self.frame_botones, image=self.img_taylor, command=self.ejecutar_taylor)
        self.boton_taylor.grid(row=0, column=2, padx=10, pady=10)

        self.boton_algos = tk.Button(self.frame_botones, image=self.img_algos, command=self.ejecutar_algoritmos)
        self.boton_algos.grid(row=0, column=3, padx=10, pady=10)

    def ejecutar_optimizacion(self):
        try:
            python_executable = os.path.join(os.getcwd(), 'VenvProject', 'Scripts', 'python.exe')
            subprocess.run([python_executable, "Optimización.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(e)
            messagebox.showerror("Error", f"No se pudo ejecutar el script de optimización: {e}")

    def ejecutar_sparse(self):
        try:
            python_executable = os.path.join(os.getcwd(), 'VenvProject', 'Scripts', 'python.exe')
            subprocess.run([python_executable, "Sparce.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el script de matrices sparse: {e}")

    def ejecutar_taylor(self):
        try:
            python_executable = os.path.join(os.getcwd(), 'VenvProject', 'Scripts', 'python.exe')
            subprocess.run([python_executable, "Taylor.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el script de Taylor: {e}")

    def ejecutar_algoritmos(self):
        try:
            python_executable = os.path.join(os.getcwd(), 'VenvProject', 'Scripts', 'python.exe')
            subprocess.run([python_executable, "OptSinRes.py"], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el script de algoritmos: {e}")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

