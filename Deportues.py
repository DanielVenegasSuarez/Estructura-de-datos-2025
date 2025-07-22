from Json import leerDeportes,escribirDeportes
class Deportes:
    def __init__(self):
        self.nombre = None
        self.paises = None

    def __str__(self):
        return f"{self.nombre}"
    
    def setGeneral(self, nom,  paises):
        self.nombre = nom
        self.paises = paises

    def get_nombre(self):
        return self.nombre

    def get_paises(self):
        return self.paises
    
    def get_info(self):
        info = (
            f"Nombre del deporte: {self.nombre}\n"
            f"Paises que participan: {', '.join(self.paises)}"
        )
        return info
    
    def guardar_deportes(self,nom,paises):
        deportes = leerDeportes()
        deportes[nom] = {
            "Paises": paises
        }
        escribirDeportes(deportes)

    def deporteExiste(self,pais):
        deportes = leerDeportes()
        if pais in deportes:
            return True
        else:
            return False
        
    def eliminarDeBase(self,deporte):
        deportes = leerDeportes()
        if deporte in deportes:
            del deportes[deporte]
            escribirDeportes(deportes)
            return True
        else:
            return False
        
    def mostrar_deporte(self, nombre_deporte):
        deportes = leerDeportes()
        if nombre_deporte in deportes:
            datos = deportes[nombre_deporte]
            info = [nombre_deporte,', '.join(datos['Paises'])]
            return info
        else:
            return "El deporte no existe en la base de datos."