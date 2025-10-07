import os
import sys

import tkinter as tk
from tkinter import filedialog


# Funcion para obtener el path del archivo
def get_patch():
    if len(sys.argv) < 2:
        # Crear ventana oculta de Tkinter
        select = tk.Tk()
        select.withdraw()
        # Abrir diálogo para seleccionar archivo
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo PDF",
            filetypes=[
                ("Texto", "*.pdf"),
            ],
        )
        select.destroy()
    else:
        ruta_archivo = sys.argv[1]
    return ruta_archivo


# Obtener Alto y ancho de la pantalla
def get_width_height(MONITORS):
    if len(MONITORS) > 1:
        FIXED_HEIGHT = MONITORS[1].height
        FIXED_WIDTH = MONITORS[1].width
    else:
        FIXED_HEIGHT = MONITORS[0].height
        FIXED_WIDTH = MONITORS[0].width
    return FIXED_HEIGHT, FIXED_WIDTH


# Crear la imagen de la primera pagina
def create_first_image(pdf, DIR):
    img = pdf[0].get_pixmap(dpi=200)
    num_page = int(pdf[0].number) + 1
    img.save(f"{DIR}\\page%i.jpg" % num_page)


# Obtenemos el directorio de el background
def get_path_bk(folder, filename):
    if getattr(sys, "frozen", False):
        # Ejecutando desde .exe
        base_path = os.path.join(sys._MEIPASS, folder)
    else:
        # Ejecutando como script normal
        base_path = os.path.join(os.getcwd(), folder)
    return os.path.join(base_path, filename)


# Método para calcular el nuevo size de la diapositiva si no es 16:9
def new_size(img, height):
    wpercent = height / float(img.height)
    new_width = int((float(img.width) * float(wpercent)))
    return (new_width, height)


# Método para calcular el nuevo size de la diapositiva si la pantalla no es 16:9
def new_size_width(img, width):
    wpercent = width / float(img.width)
    new_height = int((float(img.height) * float(wpercent)))
    return (width, new_height)


# Método para calcular la posicion donde colocar la diapositiva si no es 16:9
def position(img, width):
    return int((width - img.width) / 2)


# Método para calcular la posicion donde colocar la diapo si la pantalla no es 16:9
def position_screen(img, height):
    return int((height - img.height) / 2)


# Crear las imagenes
def create_images(pdf, DIR):
    # print(pdf[0].get_pixmap(dpi=200))
    for page in pdf:
        print("convertida")
        img = page.get_pixmap(dpi=200)
        num_page = int(page.number) + 1
        img.save(f"{DIR}\\page%i.jpg" % num_page)
