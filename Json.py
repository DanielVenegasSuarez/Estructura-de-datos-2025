from json import loads, dump
def leerUsuarios():
    with open('Usuarios.json','r', encoding="utf-8-sig") as file:
        datos = file.read()
    users = loads(datos)
    return users
def escribirUsuarios(objeto):
    with open('Usuarios.json','w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerPaises():
    with open('Paises.json','r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirPaises(objeto):
    with open('Paises.json','w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerDeportes():
    with open('Deportes.json','r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirDeportes(objeto):
    with open('Deportes.json','w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

def leerParticiapantes():
    with open('Participantes.json','r', encoding="utf-8-sig") as file:
        datos = file.read()
    country = loads(datos)
    return country
def escribirParticipantes(objeto):
    with open('Participantes.json','w', encoding="utf-8" ) as file:
        dump(objeto, file, ensure_ascii= False, indent=2)

 