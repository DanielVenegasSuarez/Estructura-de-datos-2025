import os
from Lista_Doblemente_Enlazada import *
from Diccionario_Participantes import *
from Usuarios import *
from Paises import *



class Aplicacion:
    def __init__(self):
        self.objPais = Paises()
        self.objUsuario = Usuario()

    def registrar(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        print("\n--- Registro ---")
        usuario = input("Elige un nombre de usuario: ")
        if self.objUsuario.existeUsuario(usuario):
            print("El usuario ya existe.")
            return
        contrasena = input("Elige una contraseña: ")
        self.objUsuario.guardarUsuario(usuario, contrasena)
        print("¡Usuario registrado exitosamente!")
        return

    def iniciar_sesion(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        print("\n--- Iniciar sesión ---")
        usuario = input("Usuario: ")
        contrasenna = input("Contraseña: ")
        
        print()
        if self.objUsuario.verificarContra(usuario,contrasenna) == True:
            print("¡Inicio de sesión exitoso!")
            if self.objUsuario.esAdmin(usuario) == True:
                self.programa_Olimpico(True)
            else:
                self.programa_Olimpico(False)
            return
        else:
            print("Usuario o contraseña incorrectos.")

    def programa_Olimpico(self,esAdmin):
        if esAdmin:
            print("----Inicio sesión como Administrador")
            #Agregar, eliminar y actualizar la información de los participantes
            self.programa_Olimpico_Admin()
            pass
        else:
            print("----Inicio sesión como Usuario")
            # Búsqueda avanzada de participantes
            self.programa_Olimpico_User()
            pass

    def programa_Olimpico_Admin(self):
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Gestionar pais")
            print("2. Gestionar participante")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                return self.gestionar_Paises()
            elif opcion =="2":
                return self.gestionar_Participantes()
            elif opcion == "3":
                print("Cerrando ciclo usuario")
                break
                
    def gestionar_Participantes(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Agregar participante")
            print("2. Eliminar participante")
            print("3. Modificar participante")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                self.agrega_Participante()
            elif opcion =="2":
                self.elimina_Participante()
            elif opcion == "3":
                pass
            elif opcion == "4":
                print("Cerrando ciclo usuario")
                break

    def agrega_Participante(self):       
        print("Ingrese los siguientes datos del participante:")
        nombre = input("Nombre: ")
        pais_participante = input("Pais: ")
        if self.objPais.paisExiste(pais_participante) == False:
            deporte = input("Deporte que practica: ")  
            edad = int(input("Edad del participante: "))
            genero = input("Genero (Masculino o femenino): ")
            registrarParticipantes(nombre, pais_participante, deporte, edad, genero)
            print("/n¡Se agrego un participante con exito!")
        elif pais_participante == "Cancelar": 
            return
        else:
            pais_participante= input("Ese no es un pais valido. Ingrese otro pais o 'Cancelar' para cancelar: ")

    def elimina_Participante(self):
        nombre = input("Ingrese el nombre del participante: ")
        if eliminarDeBase(nombre) == True:
            print(f"Participante {nombre} eliminado.\n")
        else:
            print(f"No se encontró al participante {nombre}.\n")

    def gestionar_Paises(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Agregar pais")
            print("2. Eliminar pais")
            print("3. Modificar pais")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                return self.agrega_Pais()
            elif opcion =="2":
                return self.elimina_pais()
            elif opcion == "3":
                pass
            elif opcion == "4":
                print("Cerrando ciclo usuario")
                break

    def agrega_Pais(self):
        print("Ingrese los siguientes datos:")
        nombre_pais = input("Nombre del pais: ")
        if not self.objPais.paisExiste(nombre_pais):
            entrada_deportes = input("Deportes (separa por comas): ")  
            deportes = [d.strip() for d in entrada_deportes.split(",")]
            self.objPais.guardar_paises(nombre_pais,deportes)
            print()
            print("¡Se agrego un pais con exito!")
        else:
            print("Ese pais ya se encuentra registrado")

    def elimina_pais(self):
        nombre_pais = input("Nombre del pais a eliminar: ")  
        
        if self.objPais.eliminarDeBase(nombre_pais) == True:
            print("Se elimino el pais con Exito")
        else:
            print("Este pais no participa en los olimpicos.")

    def programa_Olimpico_User(self):
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Buscar participante")
            print("2. Buscar competencia")
            print("3. Buscar pais")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                self.buscar_Participante()
            elif opcion =="2":
                pass
            elif opcion == "3":
                self.buscar_Pais()
            elif opcion == "4":
                print("Cerrando ciclo usuario")
                break

    def buscar_Participante(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Buscar Participante especifico")
            print("2. Mostrar todos los participantes")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                nombre = self.digitar_texto("Escriba el nombre del participante que desea buscar: ")
                parti = leerParticiapantes()
                if nombre in parti:
                    print(nombre+": "+ parti[nombre])
                else: print("Este participante no esta en los olimpicos")
            elif opcion =="2":
                os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
                print("Los atletas que participan en los olimpicos son:")
                parti = leerParticiapantes()
                for p in parti:
                    print(p+": "+ parti[p])
            elif opcion == "3":
                print("Cerrando ciclo usuario")
                break

    def buscar_Pais(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
        while True:
            print("\n¿Qué desea hacer?")
            print("\n1. Buscar Pais especifico")
            print("2. Mostrar todos los paises")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                opcion_pais = self.digitar_texto("Escriba el nombre del pais que desea buscar:  ")
                pais = self.lista_paises.find_por_nombre(opcion_pais)
                if pais != None:
                    print(pais.data.get_info())
                    return
                else:
                    print("Este pais no participa en los olimpicos.")
            elif opcion =="2":
                os.system('cls' if os.name == 'nt' else 'clear')  # Limpia terminal
                print("Los paises que participan en los olimpicos son:")
                print(self.lista_paises)
            elif opcion == "3":
                print("Cerrando ciclo usuario")
                break

    def digitar_texto(self,texto_pedido):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia pantalla (Windows o Linux/Mac)
        print()
        nombre = input(texto_pedido)
        return nombre
                
    def main(self):

        #Lista doblemente enlazada de paises
        self.lista_paises = ListaDoblementeEnlazada()
        #Se añaden unos paises de ejemplo
        pais1 = Paises()
        pais1.setGeneral("Colombia",5,["Ciclismo","Futbol","Levantamiento Pesas"])
        pais2 = Paises()
        pais2.setGeneral("Alemania",20,["Natacion","Futbol","Levantamiento Pesas"])
        pais3 = Paises()
        pais3.setGeneral("China",20,["Natacion","Futbol","Levantamiento Pesas","Ciclismo","Marcha","Tiro con arco"])
        #Participante de ejemplo
        self.lista_paises.pushBack(pais1)
        self.lista_paises.pushFront(pais2)
        pais_anterior = self.lista_paises.find(pais1)
        self.lista_paises.addAfter(pais_anterior,pais3)
        while True:
            print("\n1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                self.registrar()
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    app = Aplicacion()
    app.main()
