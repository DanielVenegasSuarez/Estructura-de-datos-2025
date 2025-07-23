import os
import sys

def obtener_ruta(nombre_relativo):
    """
    Obtiene la ruta absoluta a un recurso (archivo o carpeta)
    que está empaquetado por PyInstaller o en el directorio actual.
    """
    if hasattr(sys, '_MEIPASS'):
        # Si se ejecuta como un ejecutable de PyInstaller
        return os.path.join(sys._MEIPASS, nombre_relativo)
    # Si se ejecuta como un script Python normal
    # Usamos os.path.abspath(os.path.dirname(__file__)) para obtener la ruta del script actual
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), nombre_relativo)