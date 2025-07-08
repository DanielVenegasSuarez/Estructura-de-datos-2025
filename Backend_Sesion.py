from Json import leerUsuarios
listaU = leerUsuarios()

def validar_Usuario(nombre: str, contraseña: str):
    '''Valida si registra un usuario'''
    largoNombre = len(nombre)
    if largoNombre<1: return False, "Inserte nombre de usuario"
    if 30<largoNombre: return False, "El nombre debe tener maximo 30 caracteres"
    for x in listaU:
        if x== nombre: return False, "El nombre ya está registrado"
    
    largoContraseña = len(contraseña)
    if largoContraseña<1: return False, "Inserte una contraseña"
    if largoContraseña<6: return False, "La contraseña debe tener al menos 6 caracteres"
    if 20<largoContraseña: return False, "La contraseña debe tener maximo 20 caracteres"
    
    numero = False
    mayuscula = False
    minuscula = False
    especiales = '!¡,.-#$%&/"|<>}{[]^`+*´¨?¿'
    especial = False

    for x in contraseña:
        if x.isdigit(): numero=True
        if x.isupper(): mayuscula=True
        if x.islower(): minuscula=True
        if x in especiales: especial=True
        if (numero and mayuscula and minuscula and especial): break
    
    if not(numero): return False, "La contraseña debe tener al menos un numero"
    if not(mayuscula): return False, "La contraseña debe tener al menos una mayuscula"
    if not(minuscula): return False, "La contraseña debe tener al menos una minuscula"
    if not(especial): return False, "La contraseña debe tener al menos un caracter especial"

    return True, "se ha registrado el usuario con exito"

def iniciar_Sesion(nombre: str, contraseña:str):
    '''Valida el inicio de sesion'''
    for nombreU, usuario in listaU.items():
        if nombre == nombreU:
            if contraseña == usuario['Contraseña']: return True
            break
    return False