from json import loads, dump
from Crear_ejecutable import *
def leerUsuarios():
    with open(obtener_ruta('Usuarios.json'),'r', encoding="utf-8-sig") as file:
        datos = file.read()
    users = loads(datos)
    return users
def escribirUsuarios(objeto):
    with open(obtener_ruta('Usuarios.json'),'w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerPaises():
    with open(obtener_ruta('Paises.json'),'r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirPaises(objeto):
    with open(obtener_ruta('Paises.json'),'w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerDeportes():
    with open(obtener_ruta('Deportes.json'),'r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirDeportes(objeto):
    with open(obtener_ruta('Deportes.json'),'w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerParticiapantes():
    with open(obtener_ruta('Participantes.json'),'r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirParticipantes(objeto):
    with open(obtener_ruta('Participantes.json'),'w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

 