from Json import leerPaises,escribirPaises
class Paises:
    def __init__(self):
        self.nombre = None
        self.numeroParticipantes = None
        self.deportes = None

    def __str__(self):
        return f"{self.nombre}"

    def setGeneral(self, nom, numParticipantes, deport):
        self.nombre = nom
        self.numeroParticipantes = numParticipantes
        self.deportes = deport

    def get_nombre(self):
        return self.nombre

    def get_participantes(self):
        return self.numeroParticipantes

    def get_deportes(self):
        return self.deportes
    
    def get_info(self):
        info = (
            f"Nombre del país: {self.nombre}\n"
            f"Número de participantes: {self.numeroParticipantes}\n"
            f"Deportes en los que participa: {', '.join(self.deportes)}"
        )
        return info

    def guardar_paises(self,nom,depor):
        paises = leerPaises()
        paises[nom] = {

            "Numero de participantes": 0,
            "Deportes": depor
        }
        escribirPaises(paises)
    
    def actualizarParticipantes(self,nom):
        paises = leerPaises()
        pais = paises[nom]
        num = pais["Numero de Participantes"]
        pais["Numero de Participantes"] = num + 1
        paises[nom] = pais 
        escribirPaises()

    def paisExiste(self,pais):
        paises = leerPaises()
        if pais in paises:
            return True
        else:
            return False
        
    def deporteExistePais(self,nom,dep):
        paises = leerPaises()
        pais = paises[nom]
        if dep in pais["Deportes"]:
            return True
        else: 
            return False

    def eliminarDeBase(self,pais):
        paises = leerPaises()
        if pais in paises:
            del paises[pais]
            escribirPaises(paises)
            return True
        else:
            return False
