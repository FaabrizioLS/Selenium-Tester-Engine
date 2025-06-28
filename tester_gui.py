import tkinter as tk
from tkinter import ttk, messagebox, filedialog 
from tester_engine import run_tests 
from pathlib import Path 
import threading 

# =============================
# Establecimiento de colores 
# =============================
FONDO = "#212121" # Fondo general
CAMPOS = "#303030" # Fondo para campos de entrada
TEXTO = "#FFFFFF" # Texto blanco
BOTON = "#FFFFFF" # Fondo de botón blanco
BOTON_TEXTO = "#000000" # Texto de botón negro
BOTON_HOVER = "#DDDDDD" # Color al pasar el mouse

# ==========================
# Seleccionar archivo HTML
# ==========================
def seleccionar_archivo(): # Muestra diálogo para elegir archivo
    archivo = filedialog.askopenfilename( # Abre selector
        title="Selecciona el archivo HTML",
        filetypes=[("Archivos HTML", "*.html *.htm")]
    )
    if archivo: # Si el usuario seleccionó uno
        ruta = Path(archivo).resolve() # Resolvemos ruta absoluta
        url_formato_file = f"file:///{ruta.as_posix()}" # Formato compatible con navegador
        url_entry.delete(0, tk.END) # Borramos el contenido previo
        url_entry.insert(0, url_formato_file) # Insertamos la nueva ruta

# ====================
# Ejecutar las pruebas
# ====================
def ejecutar(): # Ejecuta validaciones al presionar el botón
    url = url_entry.get() # Obtenemos la URL escrita
    if not url: # Si está vacío
        messagebox.showwarning("Advertencia", "Por favor, ingresa una URL válida o selecciona un archivo HTML")
        return

    progressbar.pack(pady=10, fill=tk.X) # Mostramos barra de progreso
    progressbar.start() # Iniciamos la animación

    def tarea(): # Lógica que corre en segundo plano
        reporte = run_tests(url) # Ejecutamos pruebas
        output_text.delete(1.0, tk.END) # Limpiamos consola de salida
        output_text.insert(tk.END, reporte) # Mostramos resultados
        progressbar.stop() # Detenemos animación
        progressbar.pack_forget() # Ocultamos barra

    threading.Thread(target=tarea).start() # Iniciamos la tarea en segundo plano

# ========================
# Crear ventana principal
# ========================
root = tk.Tk() # Creamos ventana raíz
root.title("HTML5 Form Tester - Selenium GUI") # Título de ventana
root.geometry("800x600") # Tamaño inicial
root.configure(bg=FONDO) # Fondo en modo oscuro

# ========================
# Estilos para los widgets
# ========================
style = ttk.Style()
style.theme_use("clam") # Tema claro base (para personalizar)
style.configure("TFrame", background=FONDO) # Fondo para marcos
style.configure("TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 11)) # Etiquetas
style.configure("TButton", background=BOTON, foreground=BOTON_TEXTO, font=("Segoe UI", 10, "bold"), padding=6) # Botones
style.map("TButton", background=[("active", BOTON_HOVER)]) # Hover para botón
style.configure("TProgressbar", troughcolor="#424242", bordercolor="#333", background="#7C4DFF", lightcolor="#7C4DFF", darkcolor="#7C4DFF") # Barra de progreso

# ======================
# Contenido principal
# ======================
frame = ttk.Frame(root, padding=20, style="TFrame") # Marco principal con padding
frame.pack(fill=tk.BOTH, expand=True) # Se expande en toda la ventana

titulo_label = ttk.Label(frame, text="Formulario HTML5 - Validador Automático", font=("Segoe UI", 16, "bold")) # Título principal
titulo_label.pack(pady=(0, 15)) # Espaciado inferior

subtitulo = ttk.Label(frame, text="Selecciona o ingresa la ruta del formulario HTML5 para validar con Selenium WebDriver.") # Subtítulo descriptivo
subtitulo.pack(anchor=tk.W, pady=(0, 10)) # Alineado a la izquierda

url_label = ttk.Label(frame, text="Ruta o URL del formulario:") # Etiqueta para campo de URL
url_label.pack(anchor=tk.W) # Alineado a la izquierda

url_entry = tk.Entry(frame, width=100, bg=CAMPOS, fg=TEXTO, insertbackground=TEXTO, font=("Segoe UI", 10), relief="flat", highlightbackground=FONDO) # Campo para ingresar la ruta
url_entry.pack(fill=tk.X, pady=5) # Ocupar todo el ancho

# ===========================
# Botones: buscar y ejecutar
# ===========================
boton_frame = ttk.Frame(frame, style="TFrame") # Contenedor de botones
boton_frame.pack(fill=tk.X, pady=(5, 15)) # Margen inferior

btn_buscar = ttk.Button(boton_frame, text="📂 Buscar archivo...", command=seleccionar_archivo) # Botón para seleccionar archivo
btn_buscar.pack(side=tk.LEFT, padx=(0, 10)) # A la izquierda

btn_ejecutar = ttk.Button(boton_frame, text="▶ Ejecutar pruebas", command=ejecutar) # Botón para ejecutar pruebas
btn_ejecutar.pack(side=tk.LEFT) # A la izquierda

# =====================
# Barra de progreso
# =====================
progressbar = ttk.Progressbar(frame, mode="indeterminate") # Carga animada sin progreso definido

# =====================
# Consola de resultados
# =====================
output_text = tk.Text(frame, height=20, bg=CAMPOS, fg=TEXTO, insertbackground=TEXTO, font=("Consolas", 10), wrap=tk.WORD, borderwidth=0) # Área para mostrar resultados
output_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0)) # Ocupar todo el espacio disponible

# ====================
# Ejecutar la ventana
# ====================
root.mainloop() # Inicia la app
