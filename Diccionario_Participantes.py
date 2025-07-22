#ESTRUCTURA DE DATOS 2025-1 UNIVERSIDAD NACIONAL DE COLOMBIA
# INTEGRATES: Daniel Venegas, Luis, Miguel, Gabriel
# OLIMPICOS 2025
from Json import escribirParticipantes,leerParticiapantes

def registrarParticipantes(nombre, pais, deporte, edad, genero):
    parti = leerParticiapantes()
    parti[nombre] = {
            "Nombre": nombre,
            "Pais": pais,
            "Deporte": deporte,
            "Edad": edad,
            "Genero": genero
        }
    escribirParticipantes(parti)

def eliminarDeBase(nombre):
    base = leerParticiapantes()
    if nombre in base:
        base[nombre].pop()
        escribirParticipantes(base)
        return True
    else:
        return False

