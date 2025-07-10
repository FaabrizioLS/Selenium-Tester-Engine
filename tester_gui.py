import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
from tester_engine import run_tests  # Asegúrate que use el run_tests con parámetro navegador
from pathlib import Path
import threading

# =============================
# Establecimiento de colores
# =============================
FONDO = "#212121"
CAMPOS = "#303030"
TEXTO = "#FFFFFF"
BOTON = "#FFFFFF"
BOTON_TEXTO = "#000000"
BOTON_HOVER = "#DDDDDD"

# ==========================
# Seleccionar archivo HTML
# ==========================
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo HTML",
        filetypes=[("Archivos HTML", "*.html *.htm")]
    )
    if archivo:
        ruta = Path(archivo).resolve()
        url_formato_file = f"file:///{ruta.as_posix()}"
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url_formato_file)

# ====================
# Ejecutar las pruebas
# ====================
def ejecutar():
    url = url_entry.get()
    navegador = navegador_var.get()

    if not url:
        messagebox.showwarning("Advertencia", "Por favor, ingresa una URL válida o selecciona un archivo HTML")
        return

    progressbar.pack(pady=10, fill=tk.X)
    progressbar.start()

    def tarea():
        reporte = run_tests(url, navegador)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, reporte)
        progressbar.stop()
        progressbar.pack_forget()

    threading.Thread(target=tarea).start()

# ========================
# Crear ventana principal
# ========================
root = tk.Tk()
root.title("Selenium Tester Engine")
icono = PhotoImage(file="assets/icon.png")
root.iconphoto(False, icono)
root.geometry("800x600")
root.configure(bg=FONDO)

# ========================
# Estilos para los widgets
# ========================
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background=FONDO)
style.configure("TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 11))
style.configure("TButton", background=BOTON, foreground=BOTON_TEXTO, font=("Segoe UI", 10, "bold"), padding=6)
style.map("TButton", background=[("active", BOTON_HOVER)])
style.configure("TProgressbar", troughcolor="#424242", bordercolor="#333", background="#7C4DFF", lightcolor="#7C4DFF", darkcolor="#7C4DFF")

# ======================
# Contenido principal
# ======================
frame = ttk.Frame(root, padding=20, style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

titulo_label = ttk.Label(frame, text="Formulario HTML5 - Validador Automático", font=("Segoe UI", 16, "bold"))
titulo_label.pack(pady=(0, 15))

subtitulo = ttk.Label(frame, text="Selecciona o ingresa la ruta del formulario HTML5 para validar con Selenium WebDriver.")
subtitulo.pack(anchor=tk.W, pady=(0, 10))

url_label = ttk.Label(frame, text="Ruta o URL del formulario:")
url_label.pack(anchor=tk.W)

url_entry = tk.Entry(frame, width=100, bg=CAMPOS, fg=TEXTO, insertbackground=TEXTO, font=("Segoe UI", 10), relief="flat", highlightbackground=FONDO)
url_entry.pack(fill=tk.X, pady=5)

# ===========================
# Selector de navegador
# ===========================
navegador_label = ttk.Label(frame, text="Selecciona el navegador:")
navegador_label.pack(anchor=tk.W, pady=(10, 0))

navegador_var = tk.StringVar(value="firefox")
navegador_combo = ttk.Combobox(
    frame,
    textvariable=navegador_var,
    values=["firefox", "chrome", "edge", "brave", "vivaldi"],
    state="readonly",
    font=("Segoe UI", 10)
)
navegador_combo.pack(anchor=tk.W, pady=(0, 10))

# ===========================
# Botones: buscar y ejecutar
# ===========================
boton_frame = ttk.Frame(frame, style="TFrame")
boton_frame.pack(fill=tk.X, pady=(5, 15))

btn_buscar = ttk.Button(boton_frame, text="📂 Buscar archivo...", command=seleccionar_archivo)
btn_buscar.pack(side=tk.LEFT, padx=(0, 10))

btn_ejecutar = ttk.Button(boton_frame, text="▶ Ejecutar pruebas", command=ejecutar)
btn_ejecutar.pack(side=tk.LEFT)

# =====================
# Barra de progreso
# =====================
progressbar = ttk.Progressbar(frame, mode="indeterminate")

# =====================
# Consola de resultados
# =====================
output_text = tk.Text(frame, height=20, bg=CAMPOS, fg=TEXTO, insertbackground=TEXTO, font=("Consolas", 10), wrap=tk.WORD, borderwidth=0)
output_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

# ====================
# Ejecutar la ventana
# ====================
root.mainloop()
