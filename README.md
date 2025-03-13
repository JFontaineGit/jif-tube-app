# Jif Tube

Bienvenido al proyecto **Jif Tube**, una aplicación de música gratuita desarrollada con **Flet** para gestionar música, historiales de reproducción, playlists y favoritos.

## Requisitos

- **Python**: Versión 3.12 o superior.
- **uv**: Herramienta para gestionar entornos virtuales y dependencias (instalable vía `pip install uv`).
- **Sistema operativo**: Compatible con Windows, macOS y Linux.

## Instalación

Sigue estos pasos para configurar el entorno y ejecutar el proyecto:

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:

git clone https://github.com/tu-usuario/jif-tube.git
cd jif-tube

### 2. Instalar uv
Si aún no tienes uv instalado, instálalo globalmente con pip:

**pip install uv**

### 3. Crear un entorno virtual con uv
Crea un entorno virtual en el directorio del proyecto:

**uv venv**

Esto creará un directorio .venv con el entorno virtual.

### 4. Activar el entorno virtual
Activa el entorno virtual según tu sistema operativo:
Windows:

.venv\Scripts\activate

macOS/Linux:

source .venv/bin/activate

Una vez activado, verás (venv) al inicio de tu terminal.

5. Instalar dependencias
Instala las dependencias definidas en el archivo pyproject.toml usando uv:

**uv sync**

Esto instalará flet y cualquier otra dependencia especificada.

### 7. Ejecutar la aplicación
Ejecuta el archivo principal para iniciar la aplicación:

**python main.py**

La aplicación se abrirá en tu navegador predeterminado gracias a Flet.

### 8. Desactivar el entorno virtual (opcional)
Cuando termines, desactiva el entorno virtual:

**deactivate**

