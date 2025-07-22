from Json import escribirDeportes,leerDeportes
class Deporte:
    def __init__(self, nombre = None, categorias = {}):
        self.nombre = nombre
        self.categorias = categorias

    def setGeneral(self, nom, categorias: dict):
        self.nombre = nom
        self.categorias = categorias
    
    def agregar_categoria(self, nombre_cat, genero=None, rango_peso=None, rango_altura=None):
        """Añade o actualiza una categoría en el diccionario."""
        self.categorias[nombre_cat] = {
            'genero': genero,
            'rango_peso_kg': rango_peso,
            'rango_altura_cm': rango_altura
        }
        print(f"Categoría '{nombre_cat}' agregada/actualizada en {self.nombre}.")

    def get_identificador(self):
        return self.identificador

    def get_nombre(self):
        return self.nombre

    def get_categorias(self):
        return self.categorias

    def guardarDeporte(self):
        sports = leerDeportes()
        
        if self.nombre in sports:
            return False  # Ya existe

        sports[self.nombre] = {
            "Nombre": self.nombre,
            "Categorias": self.categorias
        }

        escribirDeportes(sports)
        return True  # Se guardó correctamente
    
    def existeDeporte(self, busqueda):
        sports = leerDeportes()
        if busqueda in sports:
            return True
        else: return False

    def obtener_categoria(self, nombre_cat):
        """Devuelve los detalles de una categoría específica."""
        categorias = self.get_categorias
        if nombre_cat in categorias: return self.categorias[nombre_cat]
        return "Categoria no encontrada"

    def mostrar_categorias(self):
        """Imprime los detalles de todas las categorías del deporte."""
        print(f"--- Categorías para {self.nombre} ---")
        if not self.categorias:
            print("Este deporte no tiene categorías definidas.")
            return
        for nombre_cat, detalles in self.categorias.items():
            print(f"Categoría: {nombre_cat}")
            if detalles['genero']:
                print(f"  Género: {detalles['genero']}")
            if detalles['rango_peso_kg']:
                print(f"  Rango de Peso: {detalles['rango_peso_kg'][0]} - {detalles['rango_peso_kg'][1]} kg")
            if detalles['rango_altura_cm']:
                print(f"  Rango de Altura: {detalles['rango_altura_cm'][0]} - {detalles['rango_altura_cm'][1]} cm")
            print("-" * 20)

        