# ComboToolPro GUI - Herramienta de Procesamiento de Combos

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

ComboToolPro GUI es una aplicación diseñada para procesar y manipular listas de combos (usuario:contraseña) con múltiples funciones útiles para pentesters y profesionales de seguridad.

## Características principales

- Eliminación de duplicados
- Extracción por dominios
- Filtrado por patrones específicos
- Estadísticas de dominios
- Organización de líneas
- División y combinación de archivos
- Interfaz gráfica moderna y fácil de usar

## Requisitos

- Python 3.8 o superior
- Windows 10/11 (recomendado)

## Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/DarkPierc/Combo-Tools.git
cd Combo-Tools
```
### 1.1 Cambiar a la rama ULP 
En la rama ULP se encuentra la última versión estable del proyecto que incluye las opciones extraer logs y buscar en logs.
Estas opciones están disponibles en la pestaña de herramientas de la interfaz gráfica.

```bash
git checkout ulp
```

### 1.2 Actualizar la rama main con los cambios remotos

```bash
git pull origin main
```


### 2. Crear y activar entorno virtual (Windows)

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```cmd
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```cmd
python main.py
```

## Generación de archivo ejecutable (.exe)

Para crear un archivo ejecutable independiente:

1. Asegúrate de tener PyInstaller instalado (viene en requirements.txt)
2. Ejecuta el script de creación:

```cmd
python crear_exe.py main.py
```

El ejecutable se generará en la carpeta `dist/` con el nombre `ComboToolProGUI.exe`.

### Opciones adicionales para crear_exe.py

- **Icono personalizado**: Coloca un archivo `.ico` con el mismo nombre que tu script o `icono.ico` en el mismo directorio
- **Ocultar consola**: El script ya incluye la opción `--noconsole` por defecto
- **Un solo archivo**: Se genera un único archivo `.exe` para facilidad de distribución

## Estructura del proyecto

```
Combo-Tools/
│
├── dist/                    # Carpeta con ejecutables generados
├── venv/                    # Entorno virtual (no incluido en repo)
│
├── main.py                  # Script principal de la aplicación
├── crear_exe.py             # Script para generar .exe
├── requirements.txt         # Dependencias del proyecto
├── README.md                # Este archivo
└── icono.ico                # Icono opcional para el ejecutable
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Soporte

Para problemas o preguntas, abre un issue en el repositorio o contacta al desarrollador.