import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

# Asegúrate de que tu archivo 'lexer.py' esté en la misma carpeta.
from lexer import analizar_codigo

# =============================================
# Temas (Paletas de Colores Modernas y Minimalistas)
# =============================================
TEMAS = {
    "claro": {
        "bg_principal": "#F5F7FA",        # Gris muy claro, casi blanco
        "bg_secundario": "#FFFFFF",       # Blanco puro para fondos de áreas
        "fg_texto": "#333333",            # Gris oscuro para texto
        "bg_entrada": "#EFEFEF",          # Gris claro para campos de entrada
        "fg_entrada": "#333333",
        "bg_titulo": "#F5F7FA",
        "color_resaltado": "#007BFF",     # Azul para botones primarios
        "color_alerta": "#DC3545",        # Rojo para alertas/limpiar
        "color_exito": "#28A745",         # Verde para analizar
        "color_hover": "#E0E0E0",         # Gris claro para hover
        "color_borde": "#DDDDDD",         # Gris para bordes sutiles
    },
    "oscuro": {
        "bg_principal": "#2B2B2B",        # Gris oscuro principal
        "bg_secundario": "#3C3F41",       # Gris ligeramente más claro para áreas
        "fg_texto": "#E0E0E0",            # Gris claro para texto
        "bg_entrada": "#1E1E1E",          # Negro muy oscuro para campos de entrada
        "fg_entrada": "#F0F0F0",
        "bg_titulo": "#2B2B2B",
        "color_resaltado": "#007BFF",     # Azul
        "color_alerta": "#DC3545",        # Rojo
        "color_exito": "#28A745",         # Verde
        "color_hover": "#505050",         # Gris oscuro para hover
        "color_borde": "#555555",         # Gris para bordes sutiles
    }
}
# Variable global para mantener el estado de ordenación de la tabla
ordenacion_actual = {}


# =============================================
# Funciones
# =============================================

# 🟢 FUNCIÓN PARA CAMBIAR EL TEMA 🟢
def cambiar_tema():
    """Alterna entre el tema claro y oscuro y aplica los colores."""
    nuevo_tema = "oscuro" if tema_actual.get() == "claro" else "claro"
    colores = TEMAS[nuevo_tema]
    
    # Configurar root y frame_superior
    root.configure(bg=colores["bg_principal"])
    frame_superior.configure(bg=colores["bg_principal"])
    
    # Títulos
    titulo.configure(bg=colores["bg_principal"], fg=colores["fg_texto"])
    subtitulo.configure(bg=colores["bg_principal"], fg=colores["fg_texto"])
    
    # Frames principales
    frame_izq.configure(bg=colores["bg_principal"])
    frame_der.configure(bg=colores["bg_principal"])
    frame_botones.configure(bg=colores["bg_principal"])
    
    # Área de código (ScrolledText)
    txt_codigo.configure(
        bg=colores["bg_entrada"], 
        fg=colores["fg_entrada"], 
        insertbackground=colores["fg_entrada"],
        highlightbackground=colores["color_borde"], 
        highlightcolor=colores["color_resaltado"]
    )

    # LabelFrame de componentes
    frame_componentes.configure(
        bg=colores["bg_principal"], 
        fg=colores["fg_texto"],
        highlightbackground=colores["color_borde"],
        highlightcolor=colores["color_borde"],
        bd=1, relief="solid" 
    )
    for widget in frame_componentes.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=colores["bg_principal"], fg=colores["fg_texto"])

    # Botón de tema (cambiar icono y color de fondo)
    btn_tema.configure(
        text="🌞" if nuevo_tema == "claro" else "🌙", 
        bg=colores["bg_principal"], 
        fg=colores["fg_texto"],
        activebackground=colores["color_hover"],
        activeforeground=colores["fg_texto"]
    )

    # Estilo del Treeview (Tabla)
    style = ttk.Style()
    style.theme_use('default') 
    
    # Colores generales del Treeview
    style.configure("Treeview", 
                    background=colores["bg_secundario"], 
                    foreground=colores["fg_texto"],
                    fieldbackground=colores["bg_secundario"],
                    bordercolor=colores["color_borde"],
                    lightcolor=colores["color_borde"],
                    darkcolor=colores["color_borde"])
    
    # Color de selección de filas
    style.map('Treeview', 
              background=[('selected', colores["color_resaltado"])],
              foreground=[('selected', 'white')])

    # Estilo de los encabezados (headings) de la tabla
    style.configure("Treeview.Heading",
                    font=('Segoe UI', 10, 'bold'),
                    background=colores["bg_principal"],
                    foreground=colores["fg_texto"],
                    relief="flat",
                    padding=(5, 5))
    style.map("Treeview.Heading", 
              background=[('active', colores["color_hover"])])

    tema_actual.set(nuevo_tema)


def analizar_codigo_en_gui():
    codigo = txt_codigo.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Entrada Vacía", "Por favor, introduce código para analizar.")
        return

    resultados = analizar_codigo(codigo)

    for i in tree.get_children():
        tree.delete(i)
    
    global ordenacion_actual
    ordenacion_actual = {}

    contadores = {
        "Palabra Reservada": 0, "Identificador": 0, "Número": 0, 
        "Cadena": 0, "Operador": 0, "Delimitador": 0, "Error Léxico": 0,
    }

    for tok in resultados:
        tree.insert("", tk.END, values=(
            tok["linea"], tok["columna"], tok["token"], tok["valor"],
            tok["categoria"], tok["longitud"]
        ))
        categoria = tok["categoria"]
        if categoria in contadores:
            contadores[categoria] += 1

    for nombre, valor in contadores.items():
        if nombre in componentes:
            componentes[nombre].set(str(valor))

def ordenar_columna(tree, col, es_numerica=False):
    global ordenacion_actual
    
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    
    current_heading_text = tree.heading(col, "text").replace(" ▲", "").replace(" ▼", "")

    if col in ordenacion_actual and ordenacion_actual[col]:
        reversa = True 
        ordenacion_actual[col] = False
        tree.heading(col, text=f"{current_heading_text} ▼") 
    else:
        reversa = False
        ordenacion_actual[col] = True
        tree.heading(col, text=f"{current_heading_text} ▲") 

    for c in tree["columns"]:
        if c != col:
            original_text = tree.heading(c, "text").replace(" ▲", "").replace(" ▼", "")
            tree.heading(c, text=original_text)

    if es_numerica:
        def clave(item):
            try:
                return float(item[0])
            except ValueError:
                return -float('inf') if reversa else float('inf') 
    else:
        def clave(item):
            return item[0].lower()

    data.sort(key=clave, reverse=reversa)

    for index, (valor, item) in enumerate(data):
        tree.move(item, '', index)


# FUNCIÓN cargar_archivo CORREGIDA 
def cargar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo", 
        # CORREGIDO: Se eliminó el filetypes duplicado.
        defaultextension=".txt", 
        filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if ruta:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            txt_codigo.delete("1.0", tk.END)
            txt_codigo.insert(tk.END, contenido)
            analizar_codigo_en_gui()
        except Exception as e:
            messagebox.showerror("Error de Archivo", f"No se pudo cargar el archivo:\n{e}")

def limpiar_resultados():
    txt_codigo.delete("1.0", tk.END) 
    for i in tree.get_children():
        tree.delete(i)
    for var in componentes.values():
        var.set("0")
    global ordenacion_actual
    ordenacion_actual = {}
    for c in tree["columns"]:
        tree.heading(c, text=tree.heading(c, "text").replace(" ▲", "").replace(" ▼", ""))


# =============================================
# Ventana principal
# =============================================
root = tk.Tk()
root.title("Analizador Léxico")
root.state('zoomed') 
root.configure(bg=TEMAS["claro"]["bg_principal"])

# Inicializar tema_actual AQUÍ
tema_actual = tk.StringVar(value="claro") 

# Contenedor para el título y el botón de tema (parte superior)
frame_superior = tk.Frame(root, bg=TEMAS["claro"]["bg_principal"])
frame_superior.pack(fill=tk.X, padx=0, pady=(0, 0))

# Título principal y subtítulo
titulo = tk.Label(frame_superior, text="Analizador Léxico", font=('Segoe UI', 18, 'bold'), bg=TEMAS["claro"]["bg_titulo"], fg=TEMAS["claro"]["fg_texto"])
titulo.pack(side=tk.LEFT, padx=20, pady=10) 
subtitulo = tk.Label(frame_superior, text="Alvaro Morel 2-17-1968", font=('Segoe UI', 10), bg=TEMAS["claro"]["bg_titulo"], fg=TEMAS["claro"]["fg_texto"])
subtitulo.pack(side=tk.LEFT, padx=(5, 0), pady=10) # Ajustado padx

# Botón de tema (usando icono para minimalismo)
btn_tema = tk.Button(frame_superior, text="🌙", command=cambiar_tema, 
                     bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"], 
                     font=('Segoe UI', 14), bd=0, relief=tk.FLAT, width=3, height=1)
btn_tema.pack(side=tk.RIGHT, padx=10, pady=10)

# Dividir la ventana en dos columnas con PanedWindow
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bd=0, relief=tk.FLAT, bg=TEMAS["claro"]["bg_principal"]) 
paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Panel izquierdo: código, botones, componentes
frame_izq = tk.Frame(paned, bg=TEMAS["claro"]["bg_principal"])
paned.add(frame_izq, width=600, minsize=400) 

# Área de código (ScrolledText)
txt_codigo = scrolledtext.ScrolledText(frame_izq, width=60, height=15, font=('Consolas', 10), 
                                      bg=TEMAS["claro"]["bg_entrada"], fg=TEMAS["claro"]["fg_entrada"], 
                                      insertbackground=TEMAS["claro"]["fg_entrada"],
                                      bd=0, relief=tk.FLAT, highlightthickness=1,
                                      highlightbackground=TEMAS["claro"]["color_borde"], 
                                      highlightcolor=TEMAS["claro"]["color_resaltado"]) 
txt_codigo.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame_botones = tk.Frame(frame_izq, bg=TEMAS["claro"]["bg_principal"])
frame_botones.pack(pady=(0, 10))

# Estilo para los botones principales
style = ttk.Style()
style.theme_use('default')

style.configure("Primary.TButton", 
                font=('Segoe UI', 10, 'bold'), 
                foreground='white', 
                background=TEMAS["claro"]["color_resaltado"],
                borderwidth=0, relief="flat", padding=(10, 5))
style.map("Primary.TButton", 
          background=[('active', TEMAS["claro"]["color_hover"])]) 

btn_cargar = ttk.Button(frame_botones, text="Cargar Archivo", command=cargar_archivo, style="Primary.TButton")
btn_cargar.grid(row=0, column=0, padx=5, pady=0) 

style.configure("Success.TButton", 
                font=('Segoe UI', 10, 'bold'), 
                foreground='white', 
                background=TEMAS["claro"]["color_exito"],
                borderwidth=0, relief="flat", padding=(10, 5))
style.map("Success.TButton", 
          background=[('active', TEMAS["claro"]["color_hover"])]) 

btn_analizar = ttk.Button(frame_botones, text="Analizar", command=analizar_codigo_en_gui, style="Success.TButton")
btn_analizar.grid(row=0, column=1, padx=5, pady=0)


# ----------------------------------------------------------------------------------
# SECCIÓN DE COMPONENTES (2 Columnas, compactada)
# ----------------------------------------------------------------------------------
componentes = {
    "Palabra Reservada": tk.StringVar(value="0"), "Identificador": tk.StringVar(value="0"), 
    "Número": tk.StringVar(value="0"), "Cadena": tk.StringVar(value="0"), 
    "Operador": tk.StringVar(value="0"), "Delimitador": tk.StringVar(value="0"), 
    "Error Léxico": tk.StringVar(value="0"),
}

frame_componentes = tk.LabelFrame(frame_izq, text="Cantidad de Componentes", font=('Segoe UI', 10, 'bold'),
                                  bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"],
                                  bd=1, relief="solid", highlightbackground=TEMAS["claro"]["color_borde"])
frame_componentes.pack(padx=10, pady=10, fill=tk.X)

n_componentes = len(componentes)
mitad = (n_componentes + 1) // 2
componentes_items = list(componentes.items())

for i in range(n_componentes):
    nombre, var = componentes_items[i]
    columna_base = 0 if i < mitad else 2 
    fila = i if i < mitad else i - mitad 
    
    # Etiqueta del nombre
    tk.Label(frame_componentes, text=f"{nombre}:", anchor="w", font=('Segoe UI', 9),
             bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"]).grid(row=fila, column=columna_base, 
                                                                   padx=(10, 2), pady=1, sticky="w")
    
    # Etiqueta del valor
    tk.Label(frame_componentes, textvariable=var, font=('Consolas', 9, 'bold'), 
             width=4, anchor="e", bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"]).grid(row=fila, column=columna_base + 1, 
                                       padx=(2, 10), pady=1, sticky="e")
# ----------------------------------------------------------------------------------

# Panel derecho: resultados (Treeview)
frame_der = tk.Frame(paned, bg=TEMAS["claro"]["bg_principal"])
paned.add(frame_der, width=600, minsize=400) 

# Estilo de la tabla
style.configure("Treeview", 
                background=TEMAS["claro"]["bg_secundario"], 
                foreground=TEMAS["claro"]["fg_texto"],
                fieldbackground=TEMAS["claro"]["bg_secundario"],
                bordercolor=TEMAS["claro"]["color_borde"],
                lightcolor=TEMAS["claro"]["color_borde"],
                darkcolor=TEMAS["claro"]["color_borde"],
                rowheight=25) 

# Estilo de los encabezados (headings) de la tabla
style.configure("Treeview.Heading",
                font=('Segoe UI', 10, 'bold'),
                background=TEMAS["claro"]["bg_principal"],
                foreground=TEMAS["claro"]["fg_texto"],
                relief="flat",
                padding=(5, 5))
style.map("Treeview.Heading", 
          background=[('active', TEMAS["claro"]["color_hover"])])

columnas = ("Línea", "Columna", "Token", "Valor", "Categoría", "Longitud")
tree = ttk.Treeview(frame_der, columns=columnas, show="headings", style="Treeview") 

# Definición de encabezados con comando de ordenación
tree.heading("Línea", text="Línea", command=lambda: ordenar_columna(tree, "Línea", True))
tree.heading("Columna", text="Columna", command=lambda: ordenar_columna(tree, "Columna", True))
tree.heading("Token", text="Token", command=lambda: ordenar_columna(tree, "Token"))
tree.heading("Valor", text="Valor", command=lambda: ordenar_columna(tree, "Valor"))
tree.heading("Categoría", text="Categoría", command=lambda: ordenar_columna(tree, "Categoría"))
tree.heading("Longitud", text="Longitud", command=lambda: ordenar_columna(tree, "Longitud", True))

tree.column("Línea", width=60, anchor="center")
tree.column("Columna", width=60, anchor="center")
tree.column("Token", width=120, anchor="center")
tree.column("Valor", width=300, anchor="w")
tree.column("Categoría", width=120, anchor="center")
tree.column("Longitud", width=60, anchor="center")
tree.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

# Botón Limpiar Resultados (estilo moderno)
style.configure("Danger.TButton", 
                font=('Segoe UI', 10, 'bold'), 
                foreground='white', 
                background=TEMAS["claro"]["color_alerta"],
                borderwidth=0, relief="flat", padding=(10, 5))
style.map("Danger.TButton", 
          background=[('active', TEMAS["claro"]["color_hover"])])

btn_limpiar = ttk.Button(frame_der, text="Limpiar Resultados", command=limpiar_resultados, style="Danger.TButton")
btn_limpiar.pack(pady=10)

# Menú principal
menu = tk.Menu(root, bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"])
root.config(menu=menu)
menu_archivo = tk.Menu(menu, tearoff=0, bg=TEMAS["claro"]["bg_principal"], fg=TEMAS["claro"]["fg_texto"])
menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Limpiar Código", command=lambda: txt_codigo.delete("1.0", tk.END))
menu_archivo.add_command(label="Cargar Archivo", command=cargar_archivo)
menu_archivo.add_separator(background=TEMAS["claro"]["color_borde"])
menu_archivo.add_command(label="Salir", command=root.destroy)


# Inicializar el tema CLARO
cambiar_tema() 
tema_actual.set("claro") 
cambiar_tema() 

# Ejecutar ventana
root.mainloop()