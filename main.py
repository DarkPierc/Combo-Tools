import customtkinter as ctk
from tkinter import simpledialog
import re
import os
import random

# Configuración de apariencia
ctk.set_appearance_mode("Dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color azul

def actualizar_salida():
    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, texto_entrada.get(1.0, ctk.END))
    actualizar_contador_lineas()

def actualizar_contador_lineas():
    lineas_entrada.set(f"Líneas Entrada: {len(texto_entrada.get(1.0, ctk.END).splitlines())}")
    lineas_salida.set(f"Líneas Salida: {len(texto_salida.get(1.0, ctk.END).splitlines())}")

# Crear ventana principal
ventana = ctk.CTk()
ventana.title("ComboToolPro GUI Curso Python")
ventana.geometry("1200x600")
ventana.resizable(True, True)

# Frame principal
frame_principal = ctk.CTkFrame(ventana)
frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

# Sección de entrada
etiqueta_entrada = ctk.CTkLabel(frame_principal, text="Entrada:")
etiqueta_entrada.grid(row=0, column=0, sticky="w", pady=5)

texto_entrada = ctk.CTkTextbox(frame_principal, wrap="word", height=15)
texto_entrada.grid(row=1, column=0, pady=5, sticky="nsew")
texto_entrada.bind("<KeyRelease>", lambda e: actualizar_contador_lineas())

# Sección de salida
etiqueta_salida = ctk.CTkLabel(frame_principal, text="Salida:")
etiqueta_salida.grid(row=2, column=0, sticky="w", pady=5)

texto_salida = ctk.CTkTextbox(frame_principal, wrap="word", height=15)
texto_salida.grid(row=3, column=0, pady=5, sticky="nsew")

# Contadores de líneas
lineas_entrada = ctk.StringVar()
etiqueta_lineas_entrada = ctk.CTkLabel(frame_principal, textvariable=lineas_entrada)
etiqueta_lineas_entrada.grid(row=0, column=0, sticky="e", pady=5)

lineas_salida = ctk.StringVar()
etiqueta_lineas_salida = ctk.CTkLabel(frame_principal, textvariable=lineas_salida)
etiqueta_lineas_salida.grid(row=2, column=0, sticky="e", pady=5)

# Funciones de los botones
def pegar_entrada():
    """Pegar contenido del portapapeles al cuadro de entrada."""
    try:
        contenido = ventana.clipboard_get()
        texto_entrada.delete(1.0, ctk.END)
        texto_entrada.insert(ctk.END, contenido)
        actualizar_contador_lineas()
    except:
        pass

def copiar_salida():
    """Copiar contenido del cuadro de salida al portapapeles."""
    contenido = texto_salida.get(1.0, ctk.END)
    ventana.clipboard_clear()
    ventana.clipboard_append(contenido)

def eliminar_duplicados():
    """Eliminar líneas duplicadas de la entrada y mostrar en salida."""
    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    lineas_unicas = list(dict.fromkeys(lineas))
    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, "\n".join(lineas_unicas))
    actualizar_contador_lineas()

def extraer_por_busqueda():
    """Extraer líneas que coincidan con un término de búsqueda."""
    termino = simpledialog.askstring("Buscar", "Ingrese el término a buscar:")
    
    if termino:
        lineas_coincidentes = [linea for linea in texto_entrada.get(1.0, ctk.END).splitlines() if termino.lower() in linea.lower()]

        with open(f"{termino}.txt", "a", encoding="utf-8") as archivo:
            for linea in lineas_coincidentes:
                archivo.write(linea + '\n')

        with open(f"{termino}.txt", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            lineas_limpias = list(dict.fromkeys(lineas))

        with open(f"{termino}.txt", "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas_limpias)
        
        texto_salida.delete(1.0, ctk.END)
        texto_salida.insert(ctk.END, ''.join(lineas_limpias))
        actualizar_contador_lineas()

def extraer_md5():
    """Extraer líneas donde el contenido después de ':' tenga exactamente 32 caracteres."""
    patron = re.compile(r":.{32}$")
    lineas_coincidentes = [linea for linea in texto_entrada.get(1.0, ctk.END).splitlines() if patron.search(linea)]

    with open("_Extraidos_MD5_.txt", "a", encoding="utf-8") as archivo:
        for linea in lineas_coincidentes:
            archivo.write(linea + '\n')

    with open("_Extraidos_MD5_.txt", "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        lineas_limpias = list(dict.fromkeys(lineas))

    with open("_Extraidos_MD5_.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(lineas_limpias)
        
    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, ''.join(lineas_limpias))
    actualizar_contador_lineas()

def mostrar_estadisticas_dominios():
    """Mostrar estadísticas de dominios en orden descendente."""
    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    dominios = [re.search(r"@(.+?)\.", linea, re.IGNORECASE) for linea in lineas]
    lista_dominios = [coincidencia.group(1).lower() for coincidencia in dominios if coincidencia]

    estadisticas = {}
    total = len(lista_dominios)
    for dominio in lista_dominios:
        if dominio not in estadisticas:
            estadisticas[dominio] = 0
        estadisticas[dominio] += 1

    estadisticas_ordenadas = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)
    
    salida = []
    for dominio, cantidad in estadisticas_ordenadas:
        porcentaje = (cantidad / total) * 100
        salida.append(f"{cantidad} líneas de {dominio} ({porcentaje:.2f}%)")

    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, '\n'.join(salida))
    actualizar_contador_lineas()

def filtrar_lineas_con_dos_puntos():
    """Filtrar líneas que contengan ':' y tengan entre 5 y 28 caracteres después."""
    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    lineas_filtradas = []
    
    for linea in lineas:
        if ":" in linea:
            _, _, despues_puntos = linea.partition(":")
            longitud = len(despues_puntos.strip())
            if 5 <= longitud <= 28:
                lineas_filtradas.append(linea)
    
    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, '\n'.join(lineas_filtradas))
    actualizar_contador_lineas()

def eliminar_despues_espacio():
    """Eliminar contenido después del primer espacio en cada línea."""
    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    lineas_procesadas = [linea.split(" ")[0] for linea in lineas]
    
    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, '\n'.join(lineas_procesadas))
    actualizar_contador_lineas()

def organizar_lineas():
    """Ofrecer opciones de organización para las líneas."""
    opcion = simpledialog.askstring("Organizar", 
        "Elija una opción:\n1. A-Z\n2. Z-A\n3. 0-9\n4. Cortas a largas\n5. Largas a cortas\n6. Aleatorizar", 
        initialvalue="1", parent=ventana)

    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    if opcion == "1":
        lineas_ordenadas = sorted(lineas)
    elif opcion == "2":
        lineas_ordenadas = sorted(lineas, reverse=True)
    elif opcion == "3":
        lineas_ordenadas = sorted(lineas, key=lambda x: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', x)])
    elif opcion == "4":
        lineas_ordenadas = sorted(lineas, key=len)
    elif opcion == "5":
        lineas_ordenadas = sorted(lineas, key=len, reverse=True)
    elif opcion == "6":
        random.shuffle(lineas)
        lineas_ordenadas = lineas
    else:
        return

    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, '\n'.join(lineas_ordenadas))
    actualizar_contador_lineas()

def dividir_por_lineas():
    """Dividir contenido en archivos según número de líneas especificado."""
    num_lineas = simpledialog.askinteger("Dividir", "¿Cuántas líneas por archivo?", parent=ventana)
    if not num_lineas:
        return
    
    nombre = simpledialog.askstring("Nombre", "¿Nombre para los archivos?", parent=ventana)
    if not nombre:
        return

    directorio = os.path.join("divididos", nombre)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    lineas = texto_entrada.get(1.0, ctk.END).splitlines()
    for indice, inicio in enumerate(range(0, len(lineas), num_lineas), 1):
        ruta_archivo = os.path.join(directorio, f"{nombre}_{indice}.txt")
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write('\n'.join(lineas[inicio:inicio + num_lineas]))

def combinar_archivos():
    """Combinar archivos de texto del directorio 'combinar'."""
    contenido_combinado = []
    directorio = "combinar"

    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):
            with open(os.path.join(directorio, archivo), "r", encoding="utf-8") as f:
                contenido_combinado.extend(f.readlines())

    with open("_combinado_.txt", "w", encoding="utf-8") as f:
        f.writelines(contenido_combinado)

    with open("_combinado_.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()
        lineas_unicas = list(dict.fromkeys(lineas))

    with open("_combinado_.txt", "w", encoding="utf-8") as f:
        f.writelines(lineas_unicas)

    texto_salida.delete(1.0, ctk.END)
    texto_salida.insert(ctk.END, ''.join(lineas_unicas))
    actualizar_contador_lineas()
    
def guardar_salida():
    """Guardar el contenido de salida en un archivo."""
    nombre_archivo = simpledialog.askstring("Guardar", "Nombre del archivo:", parent=ventana)
    
    if not nombre_archivo:
        return

    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(texto_salida.get(1.0, ctk.END))

# Frame de botones
frame_botones = ctk.CTkFrame(frame_principal)
frame_botones.grid(row=4, column=0, pady=10, sticky="ew")

# Configurar grid para que los elementos se expandan
frame_principal.grid_rowconfigure(1, weight=1)
frame_principal.grid_rowconfigure(3, weight=1)
frame_principal.grid_columnconfigure(0, weight=1)

# Botones
boton_pegar = ctk.CTkButton(frame_botones, text="Pegar Entrada", command=pegar_entrada)
boton_pegar.pack(side="left", padx=5, pady=5, expand=True)

boton_copiar = ctk.CTkButton(frame_botones, text="Copiar Salida", command=copiar_salida)
boton_copiar.pack(side="left", padx=5, pady=5, expand=True)

boton_eliminar_dup = ctk.CTkButton(frame_botones, text="Eliminar Duplicados", command=eliminar_duplicados)
boton_eliminar_dup.pack(side="left", padx=5, pady=5, expand=True)

boton_extraer = ctk.CTkButton(frame_botones, text="Extraer Dominio", command=extraer_por_busqueda)
boton_extraer.pack(side="left", padx=5, pady=5, expand=True)

boton_md5 = ctk.CTkButton(frame_botones, text="Extraer MD5", command=extraer_md5)
boton_md5.pack(side="left", padx=5, pady=5, expand=True)

boton_estadisticas = ctk.CTkButton(frame_botones, text="Estadísticas", command=mostrar_estadisticas_dominios)
boton_estadisticas.pack(side="left", padx=5, pady=5, expand=True)

# Segunda fila de botones
frame_botones2 = ctk.CTkFrame(frame_principal)
frame_botones2.grid(row=5, column=0, pady=5, sticky="ew")

boton_limpiar = ctk.CTkButton(frame_botones2, text="Limpiar", command=filtrar_lineas_con_dos_puntos)
boton_limpiar.pack(side="left", padx=5, pady=5, expand=True)

boton_eliminar_captura = ctk.CTkButton(frame_botones2, text="Eliminar Captura", command=eliminar_despues_espacio)
boton_eliminar_captura.pack(side="left", padx=5, pady=5, expand=True)

boton_organizar = ctk.CTkButton(frame_botones2, text="Organizar", command=organizar_lineas)
boton_organizar.pack(side="left", padx=5, pady=5, expand=True)

boton_dividir = ctk.CTkButton(frame_botones2, text="Dividir", command=dividir_por_lineas)
boton_dividir.pack(side="left", padx=5, pady=5, expand=True)

boton_combinar = ctk.CTkButton(frame_botones2, text="Combinar", command=combinar_archivos)
boton_combinar.pack(side="left", padx=5, pady=5, expand=True)

boton_guardar = ctk.CTkButton(frame_botones2, text="Guardar Salida", command=guardar_salida)
boton_guardar.pack(side="left", padx=5, pady=5, expand=True)

# Inicializar contador
actualizar_contador_lineas()

ventana.mainloop()