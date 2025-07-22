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

def eliminarDeBase(nombre, pais):
    base = leerParticiapantes()
    if nombre in base:
        if base[nombre]["Pais"] == pais:
            del base[nombre]
            escribirParticipantes(base)
            return True
        else:
            return False  # El nombre existe pero no corresponde al país
    return False  # El nombre no existe


def participanteExiste(nombre, pais):
    participantes = leerParticiapantes()
    if nombre in participantes and participantes[nombre]["Pais"] == pais:
        return True
    return False

        
def mostrar_participante(nombre_participante, pais):
    participantes = leerParticiapantes()
    if nombre_participante in participantes:
        datos = participantes[nombre_participante]
        if datos["Pais"] == pais:
            info = [
                nombre_participante,
                datos["Pais"],
                datos["Genero"],
                datos["Edad"],
                datos["Deporte"]
            ]
            return info
        else:
            return "El participante existe, pero no pertenece al país especificado."
    else:
        return "El participante no existe en la base de datos."
    
def buscar_participante(nombre, pais = None):
        participantes = leerParticiapantes().items()
        resultados = []
        resultados_pais = []
        for participante, info in participantes:
            if nombre in participante:
                datos = [participante, info["Pais"], info["Genero"], info["Edad"], info["Deporte"]]
                resultados.append(datos)
                if pais and info["Pais"] == pais: resultados_pais.append(datos)
        if pais:
            if resultados_pais: return resultados_pais
            return resultados
        return resultados