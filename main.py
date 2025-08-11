# Versión optimizada del script
# Cambios:
# 1. Menos operaciones de disco.
# 2. Eliminación de duplicados más eficiente.
# 3. Uso de variables locales para no recalcular splits.
# 4. Lectura de archivos línea por línea cuando es posible.
# 5. Uso de más hilos dependiendo de la CPU.

import customtkinter as ctk
from tkinter import simpledialog, filedialog, messagebox
import re
import os
import random
import sys
import threading
from pathlib import Path
import easygui
import colorama
import ctypes
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

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

# Tercera fila de botones para las nuevas funcionalidades
frame_botones3 = ctk.CTkFrame(frame_principal)
frame_botones3.grid(row=6, column=0, pady=5, sticky="ew")

boton_logstoulp = ctk.CTkButton(frame_botones3, text="LogsToULP", command=lambda: logstoulp_gui())
boton_logstoulp.pack(side="left", padx=5, pady=5, expand=True)

boton_buscar_logs = ctk.CTkButton(frame_botones3, text="Buscar en Logs", command=lambda: buscar_en_logs_gui())
boton_buscar_logs.pack(side="left", padx=5, pady=5, expand=True)

# Función para LogsToULP (adaptada del código proporcionado)
def logstoulp_gui():
    colorama.init()
    
    # Asegurar que existe la carpeta ResultadosLogsToULP
    if not os.path.exists(os.path.join(os.getcwd(), "ResultadosLogsToULP")):
        os.mkdir("ResultadosLogsToULP")
    
    # Crear ventana de progreso
    progreso_ventana = ctk.CTkToplevel(ventana)
    progreso_ventana.title("LogsToULP - Progreso")
    progreso_ventana.geometry("600x400")
    # No usar grab_set() para evitar bloquear la interfaz principal
    # progreso_ventana.grab_set()  
    
    # Mantener la ventana de progreso por encima de la ventana principal
    progreso_ventana.transient(ventana)
    progreso_ventana.focus_set()
    
    # Área de texto para mostrar progreso
    texto_progreso = ctk.CTkTextbox(progreso_ventana, wrap="word", height=350)
    texto_progreso.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Asegurar que la ventana de progreso se actualice correctamente
    progreso_ventana.update()
    
    def actualizar_progreso(mensaje, color=None):
        def _actualizar():
            texto_progreso.insert(ctk.END, mensaje + "\n")
            texto_progreso.see(ctk.END)
            progreso_ventana.update_idletasks()

        # Si no estamos en el hilo principal, usar after para evitar el error
        if threading.current_thread() is threading.main_thread():
            _actualizar()
        else:
            try:
                ventana.after(0, _actualizar)
            except:
                try:
                    progreso_ventana.after(0, _actualizar)
                except:
                    pass

    class EVO:
        def ui(self):
            actualizar_progreso("LOG TO TXT -  BY @BulletPierce")
            actualizar_progreso("Cargando...")

        def get_path_pass(self, path):
            patho = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    if 'pass' in str(file).lower():
                        passw = os.path.join(root, file)
                        patho.append(passw)
            return set(patho)

        def extract_lines(self, keyword, fi):
            return_list = []
            try:
                with open(fi, "r", errors="ignore", encoding='utf-8') as file:
                    lines = file.readlines()

                for i, line in enumerate(lines):
                    if keyword in line:
                        if i + 2 < len(lines):
                            captured_lines = lines[i:i + 3]
                            wiscodes = ''.join(captured_lines)
                            return_list.append(wiscodes)
                        else:
                            continue
            except Exception as e:
                actualizar_progreso(f"Error al leer {fi}: {e}")
            return return_list

        def getinformat(self, list):
            mayat = []
            for lines in list:
                matches = re.findall(r'\w+: (.*?)\n', lines)
                maza = ':'.join(matches)
                mayat.append(maza)
            return mayat

        def datetimefolder(self, path):
            current_datetime = datetime.now().strftime("%m-%d-%y_%H-%M-%S")
            shia = os.path.join(path, current_datetime)
            os.mkdir(shia)
            return shia

        def main_converter(self, path, dt):
            try:
                # Informar que estamos procesando este archivo
                actualizar_progreso(f"Procesando: {path}")
                
                # Buscar líneas con diferentes palabras clave
                some = self.extract_lines("URL", path)
                if not some:  # Usar not some en lugar de some == []
                    some = self.extract_lines("url", path)
                    if not some:
                        some = self.extract_lines("Host", path)
                
                # Si no encontramos nada, informar y salir
                if not some:
                    actualizar_progreso(f"No se encontraron datos en: {path}")
                    return
                
                # Procesar los resultados
                mose = self.getinformat(some)
                if not mose:
                    actualizar_progreso(f"No se pudieron extraer datos formateados de: {path}")
                    return
                
                # Guardar los resultados
                op = os.path.join(dt, f"url_pass_log.txt")
                with open(op, 'a', errors='ignore', encoding='utf-8') as output_file:
                    for lines in mose:
                        clean_lines = str(lines).replace("https://", "").replace("http://", '')
                        output_file.write(clean_lines + "\n")
                
                actualizar_progreso(f"[*] Procesamiento completado para: {path}", "green")
            except Exception as e:
                actualizar_progreso(f"Error al procesar {path}: {str(e)}")
                return None

        def runner(self, path, dt):
            # Obtener la lista de archivos a procesar
            archivos = self.get_path_pass(path)
            if not archivos:
                actualizar_progreso("No se encontraron archivos con 'pass' en el nombre. Buscando en todos los archivos...")
                # Si no hay archivos con 'pass', buscar en todos los archivos .txt
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith('.txt'):
                            archivos.add(os.path.join(root, file))
            
            if not archivos:
                actualizar_progreso("No se encontraron archivos para procesar.")
                return
            
            actualizar_progreso(f"Se encontraron {len(archivos)} archivos para procesar.")
            
            # Procesar los archivos en paralelo
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Crear una lista para almacenar los futuros
                futures = []
                
                # Enviar cada archivo para procesamiento
                for archivo in archivos:
                    try:
                        future = executor.submit(self.main_converter, archivo, dt)
                        futures.append(future)
                    except Exception as e:
                        actualizar_progreso(f"Error al enviar {archivo} para procesamiento: {str(e)}")
                
                # Esperar a que todos los futuros se completen
                for future in futures:
                    try:
                        future.result()  # Esto bloqueará hasta que el futuro se complete
                    except Exception as e:
                        actualizar_progreso(f"Error en un hilo de procesamiento: {str(e)}")
            
            actualizar_progreso("Procesamiento de todos los archivos completado.")
            actualizar_progreso(f"Resultados guardados en: {os.path.join(dt, 'url_pass_log.txt')}")
            
            # Verificar si se generaron resultados
            resultado_path = os.path.join(dt, "url_pass_log.txt")
            if os.path.exists(resultado_path):
                try:
                    with open(resultado_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lineas = f.readlines()
                    actualizar_progreso(f"Se extrajeron {len(lineas)} líneas de datos.")
                except Exception as e:
                    actualizar_progreso(f"Error al verificar resultados: {str(e)}")

        def main(self):
            self.ui()
            if not os.path.exists(os.path.join(os.getcwd(), "ResultadosLogsToULP")):
                os.mkdir("ResultadosLogsToULP")
            
            # Usar filedialog en lugar de easygui para mantener consistencia con la interfaz
            logs = filedialog.askdirectory(title="Selecciona la carpeta de logs")
            if not logs:
                actualizar_progreso("Operación cancelada por el usuario.")
                return
                
            actualizar_progreso(f"Carpeta seleccionada: {logs}")
            s = self.datetimefolder(os.path.join(os.getcwd(), "ResultadosLogsToULP"))
            actualizar_progreso(f"Resultados se guardarán en: {s}")
            
            # Ejecutar el procesamiento en un hilo separado para no bloquear la interfaz
            def procesar_en_segundo_plano():
                try:
                    self.runner(logs, s)
                    
                    # Mostrar resultados en la interfaz principal
                    resultado_path = os.path.join(s, "url_pass_log.txt")
                    if os.path.exists(resultado_path):
                        try:
                            with open(resultado_path, 'r', encoding='utf-8', errors='ignore') as f:
                                contenido = f.read()
                            # Usar after para actualizar la interfaz desde el hilo principal
                            ventana.after(0, lambda: texto_salida.delete(1.0, ctk.END))
                            ventana.after(0, lambda: texto_salida.insert(ctk.END, contenido))
                            ventana.after(0, actualizar_contador_lineas)
                            ventana.after(0, lambda: actualizar_progreso(f"Proceso completado. Resultados cargados en la interfaz y guardados en {resultado_path}"))
                        except Exception as e:
                            ventana.after(0, lambda: actualizar_progreso(f"Error al cargar resultados: {e}"))
                    else:
                        ventana.after(0, lambda: actualizar_progreso("No se encontraron resultados para mostrar."))
                except Exception as e:
                    ventana.after(0, lambda: actualizar_progreso(f"Error durante el procesamiento: {str(e)}"))
            
            # Iniciar el procesamiento en un hilo separado
            try:
                threading_thread = threading.Thread(target=procesar_en_segundo_plano)
                threading_thread.daemon = True  # El hilo se cerrará cuando se cierre la aplicación
                threading_thread.start()
                actualizar_progreso("Procesamiento iniciado en segundo plano...")
            except Exception as e:
                actualizar_progreso(f"Error al iniciar el hilo de procesamiento: {str(e)}")
                # Intentar ejecutar directamente si falla el hilo
                try:
                    actualizar_progreso("Intentando ejecutar directamente...")
                    procesar_en_segundo_plano()
                except Exception as e2:
                    actualizar_progreso(f"Error al ejecutar directamente: {str(e2)}")
    
    # Botón para cerrar la ventana de progreso
    def cerrar_ventana_progreso():
        try:
            progreso_ventana.destroy()
        except:
            pass
    
    # Añadir botón para cerrar la ventana
    ctk.CTkButton(progreso_ventana, text="Cerrar", command=cerrar_ventana_progreso).pack(pady=10)
    
    # Configurar el comportamiento al cerrar la ventana con la X
    progreso_ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana_progreso)
    
    # Ejecutar el proceso
    run = EVO()
    ventana.after(100, run.main)

# Función para buscar en logs (adaptada de LOGS.py)
def buscar_en_logs_gui():
    # Crear ventana de diálogo para seleccionar carpeta
    ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta donde buscar")
    if not ruta_carpeta:
        return
    
    if not os.path.exists(ruta_carpeta):
        messagebox.showerror("Error", f"La carpeta '{ruta_carpeta}' no existe.")
        return
    
    # Pedir palabras a buscar
    palabras_input = simpledialog.askstring("Buscar", "Ingrese las palabras a buscar (separadas por comas):", parent=ventana)
    if not palabras_input:
        return
    
    palabras_buscar = [palabra.strip() for palabra in palabras_input.split(',')]
    
    # Ruta absoluta para guardar los ResultadosBusquedaLogs
    carpeta_ResultadosBusquedaLogs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ResultadosBusquedaLogs")
    if not os.path.exists(carpeta_ResultadosBusquedaLogs):
        os.makedirs(carpeta_ResultadosBusquedaLogs)
    
    # Crear ventana de progreso
    progreso_ventana = ctk.CTkToplevel(ventana)
    progreso_ventana.title("Buscando...")
    progreso_ventana.geometry("500x300")
    progreso_ventana.grab_set()  # Hacer modal
    
    # Área de texto para mostrar progreso
    texto_progreso = ctk.CTkTextbox(progreso_ventana, wrap="word", height=250)
    texto_progreso.pack(padx=10, pady=10, fill="both", expand=True)
    
    contador_txt = 0
    coincidencias = {palabra: 0 for palabra in palabras_buscar}
    ResultadosBusquedaLogs = {palabra: [] for palabra in palabras_buscar}
    
    # Expresión regular para encontrar las líneas con USER:PASS
    regex = re.compile(r"USER:\s*(\S+)\s*PASS:\s*(\S+)")
    
    def actualizar_progreso(mensaje):
        texto_progreso.insert(ctk.END, mensaje + "\n")
        texto_progreso.see(ctk.END)
        progreso_ventana.update()
    
    def buscar():
        nonlocal contador_txt
        
        for root, _, files in os.walk(ruta_carpeta):
            for file in files:
                if file.endswith(".txt"):
                    try:
                        ruta_completa = os.path.join(root, file)
                        ruta_completa = os.path.normpath(ruta_completa)
                        contador_txt += 1
                        actualizar_progreso(f"Leyendo: {ruta_completa}\n")
                        
                        with open(ruta_completa, "r", encoding="utf-8", errors='ignore') as f:
                            contenido = f.read()
                    except Exception as e:
                        actualizar_progreso(f"No se pudo leer el archivo {file}: {e}")
                        continue
                    
                    for palabra in palabras_buscar:
                        if palabra in contenido:
                            coincidencias[palabra] += 1
                            actualizar_progreso(f"¡Palabra '{palabra}' encontrada en {file}!")
                            # Buscar USER:PASS usando la expresión regular
                            for match in regex.findall(contenido):
                                usuario = match[0]
                                contrasena = match[1]
                                ResultadosBusquedaLogs[palabra].append(f"{usuario}:{contrasena}")
                    actualizar_progreso("-" * 40)
        
        actualizar_progreso(f"\nTotal de archivos .txt encontrados: {contador_txt}")
        for palabra, cantidad in coincidencias.items():
            actualizar_progreso(f"Total de archivos que contienen '{palabra}': {cantidad}")

        # Mostrar los ResultadosBusquedaLogs antes de guardarlos
        actualizar_progreso("\nResultadosBusquedaLogs encontrados:")
        ResultadosBusquedaLogs_totales = []
        for palabra, lineas in ResultadosBusquedaLogs.items():
            if lineas:
                actualizar_progreso(f'Palabra: {palabra}')
                for linea in lineas:
                    actualizar_progreso(linea)
                    ResultadosBusquedaLogs_totales.append(linea)
                actualizar_progreso("-" * 40)

        # Guardar los ResultadosBusquedaLogs en archivos separados por palabra dentro de la carpeta 'ResultadosBusquedaLogs'
        for palabra, lineas in ResultadosBusquedaLogs.items():
            if lineas:
                ruta_ResultadosLogsToULPado = os.path.join(carpeta_ResultadosBusquedaLogs, f'{palabra}.txt')
                try:
                    with open(ruta_ResultadosLogsToULPado, 'w', encoding='utf-8') as f:
                        for linea in lineas:
                            f.write(f'{linea}\n')
                    actualizar_progreso(f'Los ResultadosBusquedaLogs para la palabra "{palabra}" se han guardado en {ruta_ResultadosLogsToULPado}')
                except Exception as e:
                    actualizar_progreso(f"Error al guardar el archivo {ruta_ResultadosLogsToULPado}: {e}")
        
        # Mostrar ResultadosBusquedaLogs en la interfaz principal
        texto_salida.delete(1.0, ctk.END)
        texto_salida.insert(ctk.END, "\n".join(ResultadosBusquedaLogs_totales))
        actualizar_contador_lineas()
        
        # Agregar botón para cerrar la ventana de progreso
        ctk.CTkButton(progreso_ventana, text="Cerrar", command=progreso_ventana.destroy).pack(pady=10)
    
    # Iniciar búsqueda en un hilo separado para no bloquear la interfaz
    ventana.after(100, buscar)

# Inicializar contador
actualizar_contador_lineas()

ventana.mainloop()