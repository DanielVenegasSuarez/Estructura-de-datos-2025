from Json import escribirUsuarios,leerUsuarios
class Usuario:
    def __init__(self):
        self.identificador = None
        self.nombre = None
        self.contrasenna = None
        self.admin = bool

    def setGeneral(self, id, nom, contra, adm):
        self.identificador = id
        self.nombre = nom
        self.contrasenna = contra
        self.admin = adm

    def get_identificador(self):
        return self.identificador

    def get_nombre(self):
        return self.nombre

    def get_contrasenna(self):
        return self.contrasenna

    def guardarUsuario(self,nom,contra):
        users = leerUsuarios()

        users[self.nombre] = {
            "Identificador": len(users),
            "Nombre": nom,
            "Contraseña": contra,
            "Admin": False
        }
        escribirUsuarios(users)
    
    def existeUsuario(self, busqueda):
        users = leerUsuarios()
        if busqueda in users:
            return True
        else: return False
        
    def esAdmin(self, nom):
        users = leerUsuarios()
        user = users[nom]
        return user["Admin"]

    def verificarContra(self, nom, contra):
        users = leerUsuarios()
        usuario = Usuario()
        if usuario.existeUsuario(nom) == True :
            user = users[nom]
            usuario.setGeneral(user["Identificador"],user["Nombre"],user["Contraseña"],user["Admin"])
            if user['Contraseña'] == contra:
                return True
            else:
                return False
        else: return False

