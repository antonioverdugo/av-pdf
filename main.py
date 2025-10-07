import os
import sys
import threading
import tkinter as tk
import traceback
import multiprocessing
import tkinter.messagebox as messagebox

import fitz
from PIL import Image, ImageTk
from screeninfo import get_monitors
from multiprocessing import Pool
from tkinter import PhotoImage
import ctypes
import time

from functions import (
    get_patch,
    get_width_height,
    create_first_image,
    get_path_bk,
    new_size,
    new_size_width,
    position,
    position_screen,
)

DPI = 200
DIR = "C:\\av-pdf"
stop_flag = False
task_thread = None
process = None

# Constantes de Windows API para estilos de ventana
GWL_STYLE = -16
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_POPUP = 0x80000000


def remove_window_decorations(hwnd):
    # Obtiene estilo actual
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    # Elimina WS_OVERLAPPEDWINDOW (bordes, barra título)
    style = style & ~WS_OVERLAPPEDWINDOW
    # Añade WS_POPUP (ventana sin bordes)
    style = style | WS_POPUP
    # Aplica el nuevo estilo
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    # Actualiza ventana para aplicar cambios
    ctypes.windll.user32.SetWindowPos(
        hwnd, 0, 0, 0, 0, 0, 0x027
    )  # SWP_FRAMECHANGED=0x20 + SWP_NOMOVE|NOSIZE|NOZORDER=0x7


def fade_in(window, step=0.05, delay=0.005):
    """Desvanece la ventana desde transparente hasta completamente visible."""
    alpha = 0.0
    while alpha < 1.0:
        window.attributes("-alpha", alpha)
        window.update()
        time.sleep(delay)
        alpha += step
    window.attributes("-alpha", 1.0)


def fade_out(window, step=0.05, delay=0.02):
    """Desvanece la ventana desde visible hasta transparente, luego la cierra."""
    alpha = 1.0
    while alpha > 0:
        window.attributes("-alpha", alpha)
        window.update()
        time.sleep(delay)
        alpha -= step
    window.destroy()


# Variables globales (se usarán dentro del main)
image_id, background, new_image = None, None, None
index = 1  # Página actual
aspect = None
page = None
bk = None
canvas = None
FIXED_HEIGHT, FIXED_WIDTH = None, None


def get_resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso (funciona en dev y en PyInstaller)."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_icon_path(relative_path):
    """Devuelve la ruta absoluta, compatible con PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def convert_page(args):
    pdf_path, page_idx = args
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(dpi=DPI)
        output_path = os.path.join(DIR, f"page{page_idx + 1}.jpg")
        pix.save(output_path)
        print(f"Página {page_idx + 1} convertida y guardada.")
        return output_path
    except Exception as e:
        print(f"Error en convert_page: {e}")
        return None


def multi_thearing_task(pdf_path, total_pages):
    global stop_flag, process
    with Pool(processes=2) as pool:
        process = pool
        args = [
            (pdf_path, i) for i in range(1, total_pages)
        ]  # desde página 2 en adelante
        try:
            pool.map(convert_page, args)
        except Exception as e:
            print(f"Proceso cancelado: {e}")


def throw_heavy_task(pdf_path, total_pages):
    global task_thread
    task_thread = threading.Thread(
        target=multi_thearing_task, args=(pdf_path, total_pages), daemon=True
    )
    task_thread.start()


def shown_image(page_num):
    global background, page, new_image, image_id, canvas, aspect, bk

    img_path = os.path.join(DIR, f"page{page_num}.jpg")

    if not os.path.exists(img_path):
        print(f"Imagen {img_path} no encontrada aún.")
        return

    page = Image.open(img_path).convert("RGBA")

    width, height = page.size
    aspect = round((width / height), 2)
    aspect_screen = round((FIXED_WIDTH / FIXED_HEIGHT), 2)

    if (
        aspect == 1.78 and aspect_screen == 1.78
    ):  # Si el aspecto de pdf e screen es 16:9
        page_resized = page.resize((FIXED_WIDTH, FIXED_HEIGHT))
        background = ImageTk.PhotoImage(page_resized)
    elif (
        aspect_screen != 1.78 and aspect == 1.78
    ):  # Si el aspecto de la screen no es 16:9 pero el pdf si
        new_image = Image.new("RGB", (FIXED_WIDTH, FIXED_HEIGHT))
        new_image.paste(bk, (0, 0))
        size = new_size_width(page, FIXED_WIDTH)
        print(size[0])
        page_resized = page.resize(size)
        position_y = position_screen(page_resized, FIXED_HEIGHT)
        new_image.paste(page_resized, (0, position_y))
        background = ImageTk.PhotoImage(new_image)
    else:  # Cuando ni el aspecto del screen ni del pdf es 16:9
        new_image = Image.new("RGB", (FIXED_WIDTH, FIXED_HEIGHT))
        new_image.paste(bk, (0, 0))
        size = new_size(page, FIXED_HEIGHT)
        page_resized = page.resize(size)
        position_x = position(page_resized, FIXED_WIDTH)
        new_image.paste(page_resized, (position_x, 0))
        background = ImageTk.PhotoImage(new_image)

    canvas.itemconfig(image_id, image=background)


def next_image(event=None):
    global index
    images = os.listdir(DIR)
    max_index = len(images)
    if index < max_index:
        index += 1
        shown_image(index)
    else:
        print("No hay más imágenes.")


def prev_image(event=None):
    global index
    if index > 1:
        index -= 1
        shown_image(index)
    else:
        print("No hay más imágenes.")


def close(event=None):
    global stop_flag, task_thread, process
    stop_flag = True
    print("Cancelando tarea pesada...")
    root.destroy()
    if process:
        process.terminate()
        process.join()
        print("Multiprocessing pool terminado.")

    if task_thread and task_thread.is_alive():
        task_thread.join(timeout=1)
        print("Thread de tarea pesada finalizado.")

    for image in os.listdir(DIR):
        try:
            os.remove(os.path.join(DIR, image))
        except Exception as e:
            print(f"Error eliminando {image}: {e}")


def run_app():
    global FIXED_HEIGHT, FIXED_WIDTH, root, canvas, bk, image_id

    MONITORS = get_monitors()
    FIXED_HEIGHT, FIXED_WIDTH = get_width_height(MONITORS)
    PATH_PDF = get_patch()

    if not PATH_PDF:
        print("Selección de archivo cancelada por el usuario.")
        return

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    for image in os.listdir(DIR):
        os.remove(os.path.join(DIR, image))

    pdf = fitz.open(PATH_PDF)
    total_pages = pdf.page_count

    create_first_image(pdf, DIR)

    root = tk.Tk()
    icon_path = get_resource_path("icono.ico")
    root.iconbitmap(icon_path)
    root.config(cursor="none")
    root.configure(bg="black")
    root.attributes("-alpha", 0.0)  # Comienza invisible
    icon_path = get_resource_path("icono_16.png")
    icono = PhotoImage(file=icon_path)
    root.iconphoto(True, icono)
    root.title("Av-PDF")

    # Asegurar el icono en windows
    if sys.platform == "win64":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AvPDF.App.1.2")

    # Obtener el monitor el integrado o el extendido
    if len(MONITORS) > 1:
        monitor_ext = MONITORS[1]
        # Posicionamos la ventana al segundo monitor con el tamaño completo de él
        root.geometry(
            f"{monitor_ext.width}x{monitor_ext.height}+{monitor_ext.x}+{monitor_ext.y}"
        )
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        remove_window_decorations(hwnd)
    else:
        monitor_ext = MONITORS[0]
        # Posicionamos la ventana al segundo monitor con el tamaño completo de él
        root.geometry(f"{monitor_ext.width}x{monitor_ext.height}+0+0")
        # Poner la ventana a fullscreen
        root.attributes("-fullscreen", True)

    # Poner el foco en la ventana
    root.after(100, root.focus_force)
    # Poner la ventana sobre todas las demas
    root.attributes("-topmost", 1)

    # Mostrar ventana antes de cambiar estilos para que exista el HWND
    root.update()
    fade_in(root)

    bk_path = get_path_bk("resource", "background.jpg")
    bk = Image.open(bk_path)

    canvas = tk.Canvas(
        root,
        width=FIXED_WIDTH,
        height=FIXED_HEIGHT,
        bd=0,
        highlightthickness=0,
        relief="flat",
    )
    canvas.pack(fill="both", expand=True, padx=0)

    shown_image(index)
    image_id = canvas.create_image(0, 0, image=background, anchor="nw")

    throw_heavy_task(PATH_PDF, total_pages)

    root.bind("<Up>", next_image)
    root.bind("<Right>", next_image)
    root.bind("<Next>", next_image)
    root.bind("<Return>", next_image)
    root.bind("<space>", next_image)
    root.bind("<Button-1>", next_image)

    root.bind("<Down>", prev_image)
    root.bind("<Left>", prev_image)
    root.bind("<Prior>", prev_image)

    root.bind("<Escape>", lambda e: fade_out(root))

    root.mainloop()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        run_app()
    except Exception as e:
        error_msg = traceback.format_exc()
        print("ERROR:\n", error_msg)
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(error_msg)
        try:
            messagebox.showerror("Error", error_msg)
        except:
            pass
