from cx_Freeze import setup, Executable

# Archivos adicionales necesarios (como config.py o cualquier otro recurso)
files = ['config.py']

# Configuración del ejecutable
target = Executable(
    script="app.py",
    base="Console",  # Cambiar a "Win32GUI" si no quieres una consola de fondo
    target_name="MiApp.exe"  # Nombre del ejecutable
)

setup(
    name="Mi Aplicación Flask",
    version="1.0",
    description="Aplicación Flask ejecutada en segundo plano",
    options={"build_exe": {"include_files": files}},
    executables=[target]
)
