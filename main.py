import random
from collections import defaultdict
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtUiTools import *
from Usuarios import *
from Paises import Paises
from Deportues import Deportes
from Lista_Doblemente_Enlazada import *
import Diccionario_Participantes as Participantes
import Backend_Sesion as backend_sesion
import Json as json
from Crear_ejecutable import *


class MatchupGenerator:
    @staticmethod
    def generar_emparejamientos():
        participantes = Participantes.leerParticiapantes()
        
        categories = defaultdict(list)
        
        for nombre, datos in participantes.items():
            deporte = datos["Deporte"]
            genero = datos["Genero"]
            
            key = (deporte, genero)
            categories[key].append(nombre)
        
        emparejamientos = []
        for category, athletes in categories.items():
            if len(athletes) < 2:
                continue  
                
            random.shuffle(athletes)
            
            for i in range(0, len(athletes), 2):
                if i+1 < len(athletes):
                    emparejamientos.append({
                        'category': f"{category[0]} ({category[1]})",
                        'athlete1': athletes[i],
                        'athlete2': athletes[i+1]
                    })
        
        return emparejamientos

class MiApp(QObject):
    def __init__(self):
        
        super().__init__()
        loader = QUiLoader()
        file = QFile(obtener_ruta("diseño_olimpicos.ui"))
        file.open(QFile.ReadOnly)
        self.ui_Main = loader.load(file)
        file.close()
        file2 = QFile(obtener_ruta("diseño_inicioSesion.ui"))
        file2.open(QFile.ReadOnly)
        self.ui_inicioSesion = loader.load(file2)
        file2.close()
        file3 = QFile(obtener_ruta("dialog_emparejamientos.ui"))
        file3.open(QFile.ReadOnly)
        self.ui_matchups = loader.load(file3, None)  # Add None as parent parameter
        file3.close()
        
        if not hasattr(self, 'ui_matchups'):
            print("Error: Failed to load matchups dialog UI")
    


        # Crear una lista doblemente enlazada (en memoria)
        self.lista_paises = ListaDoblementeEnlazada()
        #Configura paises y usuarios y deportes
        self.objPais = Paises.Paises()
        self.objDeporte = Deportes()
        self.objUsuario = Usuario()

        # Configurar ventanas sin bordes
        self.ui_inicioSesion.setWindowFlag(Qt.FramelessWindowHint)
        self.ui_inicioSesion.setWindowOpacity(1)
        self.ui_Main.setWindowFlag(Qt.FramelessWindowHint)
        self.ui_Main.setWindowOpacity(1)

        # SizeGrip para redimensionar (soolo para ventana principal)
        self.grip = QSizeGrip(self.ui_Main)
        self.grip.resize(20, 20)

        # Mover ventanas
        self.clickPosition = None
        self.frame_superior_main = self.ui_Main.findChild(QWidget, "frame_Superior")
        if self.frame_superior_main:
            self.frame_superior_main.installEventFilter(self)
        self.frame_superior_inicioSesion = self.ui_inicioSesion.findChild(QWidget, "frame_Superior")
        if self.frame_superior_inicioSesion:
            self.frame_superior_inicioSesion.installEventFilter(self)

        #Control barra de titulos
        self.ui_Main.btn_Minimizar.clicked.connect(lambda: self.control_bt_minimizar(self.ui_Main))
        self.ui_Main.btn_Restaurar.clicked.connect(self.control_bt_normal)
        self.ui_Main.btn_Maximizar.clicked.connect(self.control_bt_maximizar)
        self.ui_Main.btn_Cerrar.clicked.connect(lambda: self.close_Program(self.ui_Main))

        self.ui_Main.btn_Restaurar.hide()

        self.ui_inicioSesion.btn_Minimizar.clicked.connect(lambda:self.control_bt_minimizar(self.ui_inicioSesion))
        self.ui_inicioSesion.btn_Cerrar.clicked.connect(lambda:self.close_Program(self.ui_inicioSesion))

        self.carga_Inicio_Sesion()
        

        #INTERFAZ USUARIO
        self.carga_Interfaz_Usuario()

        #INTERFAZ ADMINISTRADOR
        self.carga_Interfaz_Admin()
        
        
    def carga_Inicio_Sesion(self):
        self.ui_inicioSesion.page_inicio_sesion_labelBtn_crearNuevaCuenta.linkActivated.connect(self.abrir_ventana_registro)
        self.ui_inicioSesion.page_inicio_sesion_btn_iniciarSesion.clicked.connect(self.inicio_sesion)
    def abrir_ventana_registro(self):
        self.ui_inicioSesion.stackedWidget.setCurrentWidget(self.ui_inicioSesion.page_registrarse)
        self.ui_inicioSesion.page_registrarse_btn_registrarse.clicked.connect(self.registro)
    def inicio_sesion(self):
        usuario = self.ui_inicioSesion.page_inicio_sesion_lineEdit_nombreUsuario.text()
        contrasenna = self.ui_inicioSesion.page_inicio_sesion_lineEdit_contrasenna.text()
        if self.objUsuario.verificarContra(usuario,contrasenna):
            if self.objUsuario.esAdmin(usuario) == True:
                self.ui_inicioSesion.close()
                self.ui_Main.show()
                self.ui_Main.user_stackedWidget_main.setCurrentWidget(self.ui_Main.page_administrador)
            else:
                self.ui_inicioSesion.close()
                self.ui_Main.show() 
                self.ui_Main.user_stackedWidget_main.setCurrentWidget(self.ui_Main.page_usuario)
        else:
            QMessageBox.warning(None, "Error", "Usuario o contraseña incorrectos.")

    def registro(self):
        usuario = self.ui_inicioSesion.page_registrarse_lineEdit_nombreUsuario.text()
        contrasenna = self.ui_inicioSesion.page_registrarse_lineEdit_contrasenna.text()
        valido, mensaje = backend_sesion.validar_Usuario(usuario, contrasenna)
        if valido:
            if self.objUsuario.guardarUsuario(usuario, contrasenna):
                QMessageBox.information(None, "Éxito", mensaje)
                self.ui_inicioSesion.stackedWidget.setCurrentWidget(self.ui_inicioSesion.page_inicio_sesion)
            else:
                QMessageBox.warning(None, "Error", mensaje)
        else:
            QMessageBox.warning(None, "Error", mensaje)


    def generar_emparejamientos(self):
        try:
            matchups = MatchupGenerator.generar_emparejamientos()
            
            if not matchups:
                QMessageBox.information(self.ui_Main, "Información", 
                                    "No hay suficientes atletas para generar emparejamientos.")
                return
            
            print(f"Generated {len(matchups)} matchups")
            
            if not hasattr(self, 'ui_matchups'):
                print("Error: Matchups UI not loaded")
                return
                
            table = self.ui_matchups.findChild(QTableWidget, "table_emparejamientos")
            btn_close = self.ui_matchups.findChild(QPushButton, "btn_cerrar_emparejamientos")
            
            if not table:
                print("Error: Could not find table_emparejamientos")
                return
            if not btn_close:
                print("Error: Could not find btn_cerrar_emparejamientos")
                return
        
            table.setRowCount(0)  
            table.setRowCount(len(matchups))
            table.setHorizontalHeaderLabels(["Deporte (Género)", "Atleta 1", "Atleta 2"])
            
            for row, matchup in enumerate(matchups):
                table.setItem(row, 0, QTableWidgetItem(matchup['category']))
                table.setItem(row, 1, QTableWidgetItem(matchup['athlete1']))
                table.setItem(row, 2, QTableWidgetItem(matchup['athlete2']))
            
            table.resizeColumnsToContents()
            
            btn_close.clicked.connect(self.ui_matchups.close)
            
            self.ui_matchups.exec()
            
        except Exception as e:
            print(f"Error in generar_emparejamientos: {str(e)}")
            QMessageBox.critical(self.ui_Main, "Error", f"Ocurrió un error: {str(e)}")

    def carga_Interfaz_Usuario(self):
        #Configura el comboBox FiltrarPor
        self.ui_Main.usuario_combobox_buscarPor.addItems(["Pais","Atleta","Deporte"])
        # Conectar el evento de cambio de selección con la función que lo maneja
        self.ui_Main.usuario_combobox_buscarPor.currentIndexChanged.connect(self.seleccion_Cambiada_Usuario)
        #Configura tablas de Participante,Deporte y Pais
            # Configurar los encabezados para que se ajusten automáticamente al tamaño de la ventana
        header_deporte = self.ui_Main.user_stacketWidget_pageDeporte_table.horizontalHeader()
        header_deporte.setSectionResizeMode(QHeaderView.Stretch)
        header_pais = self.ui_Main.user_stacketWidget_pagePais_table.horizontalHeader()
        header_pais.setSectionResizeMode(QHeaderView.Stretch)
        header_participante = self.ui_Main.user_stacketWidget_pageParticipante_table.horizontalHeader()
        header_participante.setSectionResizeMode(QHeaderView.Stretch)
        #Carga pagina Pais en User
        self.carga_User_PagePais()
        #Carga pagina Participantes
        self.carga_User_PageParticipantes()
    def carga_User_PagePais(self):
        self.ui_Main.user_stacketWidget_pagePais_btnBuscar.clicked.connect(lambda:self.busca_pais("user"))
    def carga_User_PageParticipantes(self):
        self.ui_Main.user_stacketWidget_pageParticipante_btnBuscar.clicked.connect(lambda:self.busca_participante("user"))

    def seleccion_Cambiada_Usuario(self):
        seleccion = self.ui_Main.usuario_combobox_buscarPor.currentText()  # Obtener el texto seleccionado
        if seleccion == "Atleta":
            self.ui_Main.user_stackedWidged_secundary.setCurrentWidget(self.ui_Main.user_stacketWidget_page_participante)
        if seleccion == "Pais":
            self.ui_Main.user_stackedWidged_secundary.setCurrentWidget(self.ui_Main.user_stacketWidget_page_pais)
        if seleccion == "Deporte":
            self.ui_Main.user_stackedWidged_secundary.setCurrentWidget(self.ui_Main.user_stacketWidget_page_deporte)
        
    def carga_Interfaz_Admin(self):
        # Add matchup generation button
        self.ui_Main.admin_btn_generarEmparejamientos = QPushButton("Generar Emparejamientos")
        self.ui_Main.admin_btn_generarEmparejamientos.setStyleSheet("""
            QPushButton{
                font: 75 12pt "Arial";
                color: black;
                background-color:rgb(193, 193, 193);
                border:1px solid black;
            }
            QPushButton:hover{
                background-color:white;
                font: 75 12pt "Arial";
            }
        """)
        self.ui_Main.admin_btn_generarEmparejamientos.clicked.connect(self.generar_emparejamientos)
        
        btn_emparejamientos = self.ui_Main.findChild(QPushButton, "admin_btn_generarEmparejamientos")
        if btn_emparejamientos:
            btn_emparejamientos.clicked.connect(self.generar_emparejamientos)
            print("Matchups button connected successfully")
        else:
            print("Error: Could not find admin_btn_generarEmparejamientos")
        #Configura el comboBox FiltrarPor
        self.ui_Main.admin_combobox_filtrarPor.addItems(["Pais","Atleta","Deporte"])
        # Conectar el evento de cambio de selección con la función que lo maneja
        self.ui_Main.admin_combobox_filtrarPor.currentIndexChanged.connect(self.seleccion_Cambiada_Admin)
        # Establecer el índice inicial en el primer elemento
        self.ui_Main.admin_combobox_filtrarPor.setCurrentIndex(0)
        #Configura tablas de Participante,Deporte y Pais
            # Configurar los encabezados para que se ajusten automáticamente al tamaño de la ventana
        header_deporte = self.ui_Main.admin_stacketWidget_pageDeporte_table.horizontalHeader()
        header_deporte.setSectionResizeMode(QHeaderView.Stretch)
        header_pais = self.ui_Main.admin_stacketWidget_pagePais_table.horizontalHeader()
        header_pais.setSectionResizeMode(QHeaderView.Stretch)
        header_participante = self.ui_Main.admin_stacketWidget_pageParticipante_table.horizontalHeader()
        header_participante.setSectionResizeMode(QHeaderView.Stretch)
        #Carga pagina Pais en Admin
        self.carga_Admin_PagePais()
        #Carga pagina Participantes
        self.carga_Admin_PageParticipante()
        #Carga pagina Deportes 
        self.carga_Admin_PageDeportes()
    def carga_Admin_PageDeportes(self):
        self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_paises.installEventFilter(self)
        self.ui_Main.admin_stacketWidget_pageDeporte_btnGuardar.clicked.connect(self.guarda_deporte)
        self.ui_Main.admin_stacketWidget_pageDeporte_btnEliminar.clicked.connect(self.elimina_deporte)
        self.ui_Main.admin_stacketWidget_pageDeporte_btnBuscar.clicked.connect(lambda:self.busca_deporte("admin"))
        tabla = getattr(self.ui_Main, f"admin_stacketWidget_pageDeporte_table")
        tabla.cellClicked.connect(self.celda_clickeada)
    def abrirVentanaPaises(self):
        dialog = VentanaPaises(self.ui_Main)
        if dialog.exec():
            texto = dialog.obtenerTexto()
            paises = [d.strip() for d in texto.split(",") if d.strip()]
            self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_paises.setText(", ".join(paises))
    def celda_clickeada(self, fila, columna):
         if fila == 0 and columna == 2:
            self.muestraLlaves()
    def muestraLlaves(self):
        # Cada elemento representa un partido (inicialmente vacío)
        semis_izquierda = [None] * 15
        semis_derecha = [None] * 15
        # Las hojas son los equipos, que se podrían guardar por separado
        equipos_izquierda = ["BRA", "ARG", "FRA", "GER", "ESP", "ENG", "POR", "NED"]
        equipos_derecha = ["ITA", "URU", "CRO", "BEL", "JPN", "SEN", "KOR", "USA"]
        for i in range(8):
            semis_izquierda[14-i] = equipos_izquierda[i]
        for i in range(15):
            print(semis_izquierda[i])
                
        
    
    def guarda_deporte(self):
        nombre_deporte= self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_deporte.text()
        paises = self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_paises.text()
        lista_paises = [d.strip() for d in paises.split(",") if d.strip()]
        # Verificar si ya existe
        if not self.objDeporte.deporteExiste(nombre_deporte):
            self.objDeporte.guardar_deportes(nombre_deporte,lista_paises)
            QMessageBox.information(None, "Éxito", "Deporte guardado correctamente.")
        else:
            QMessageBox.information(None, "Error", "El deporte ya existe.")
    def elimina_deporte(self):
        nombre_deporte = self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_deporte.text() 
        if self.objDeporte.eliminarDeBase(nombre_deporte) == True:
            QMessageBox.information(None, "Éxito", "Se eliminó el deporte con Exito")
        else:
            QMessageBox.information(None, "Error", "Este pais no participa en los olimpicos.")
    def busca_deporte(self,modo):
        lineEdit_deporte = getattr(self.ui_Main, f"{modo}_stacketWidget_pageDeporte_lineEdit_deporte")
        tabla = getattr(self.ui_Main, f"{modo}_stacketWidget_pageDeporte_table")
        #Conseguir el nombre de deporte insertado
        nombre_deporte = lineEdit_deporte.text()
        #Vaciar la tabla
        tabla.setRowCount(0)
        #Buscar
        busqueda = self.objDeporte.buscar_deporte(nombre_deporte.upper())
        #Si no se encuentra
        if not busqueda:
            tabla.setRowCount(0)
            return QMessageBox.information(None, "Error", "El deporte no existe")
        #LLenar la tabla con los resultados
        for i in range(len(busqueda)):
            tabla.insertRow(i)
            for j in range(2):
                item = QTableWidgetItem(str(busqueda[i][j]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                tabla.setItem(i, j, item)

        
    def carga_Admin_PagePais(self):
        self.ui_Main.admin_stacketWidget_pagePais_lineEdit_deportes.installEventFilter(self)
        self.ui_Main.admin_stacketWidget_pagePais_btnGuardar.clicked.connect(self.guarda_pais)
        self.ui_Main.admin_stacketWidget_pagePais_btnEliminar.clicked.connect(self.elimina_pais)
        self.ui_Main.admin_stacketWidget_pagePais_btnBuscar.clicked.connect(lambda:self.busca_pais("admin"))
    def abrirVentanaDeportes(self):
        dialog = VentanaDeportes(self.ui_Main)
        if dialog.exec():
            texto = dialog.obtenerTexto()
            deportes = [d.strip() for d in texto.split(",") if d.strip()]
            self.ui_Main.admin_stacketWidget_pagePais_lineEdit_deportes.setText(", ".join(deportes))
    

    def guarda_pais(self):
        nombre_pais = self.ui_Main.admin_stacketWidget_pagePais_lineEdit_pais.text()
        numero_participantes = self.ui_Main.admin_stacketWidget_pagePais_lineEdit_numeroParticipantes.text()
        deportes = self.ui_Main.admin_stacketWidget_pagePais_lineEdit_deportes.text()
        lista_deportes = [d.strip() for d in deportes.split(",") if d.strip()]
        # Verificar si ya existe
        if not self.objPais.paisExiste(nombre_pais):
            self.objPais.guardar_paises(nombre_pais,numero_participantes,lista_deportes)
            QMessageBox.information(None, "Éxito", "País guardado correctamente.")
        else:
            QMessageBox.information(None, "Error", "El país ya existe.")
    def elimina_pais(self):
        nombre_pais = self.ui_Main.admin_stacketWidget_pagePais_lineEdit_pais.text() 
        if self.objPais.eliminarDeBase(nombre_pais) == True:
            QMessageBox.information(None, "Éxito", "Se eliminó el pais con Exito")
        else:
            QMessageBox.information(None, "Error", "Este pais no participa en los olimpicos.")
    def busca_pais(self,modo):
        lineEdit_pais = getattr(self.ui_Main, f"{modo}_stacketWidget_pagePais_lineEdit_pais")
        tabla = getattr(self.ui_Main, f"{modo}_stacketWidget_pagePais_table")
        #Conseguir el nombre de pais insertado
        nombre_pais = lineEdit_pais.text()
        #Vaciar la tabla
        tabla.setRowCount(0)
        #Buscar
        busqueda = self.objPais.buscar_pais(nombre_pais)
        #Si no se encuentra
        if not busqueda:
            tabla.setRowCount(0)
            return QMessageBox.information(None, "Error", "El país no existe")
        #LLenar la tabla con los resultados
        for i in range(len(busqueda)):
            tabla.insertRow(i)
            for j in range(3):
                item = QTableWidgetItem(str(busqueda[i][j]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                tabla.setItem(i, j, item)
        


    def carga_Admin_PageParticipante(self):
        self.ui_Main.admin_stackedWidget_combobox_pageParticipante_genero.addItem("Masculino","Femenino")
        self.ui_Main.admin_stacketWidget_pageParticipante_btnGuardar.clicked.connect(self.guarda_participante)
        self.ui_Main.admin_stacketWidget_pageParticipante_btnEliminar.clicked.connect(self.elimina_participante)
        self.ui_Main.admin_stacketWidget_pageParticipante_btnBuscar.clicked.connect(lambda:self.busca_participante("admin"))
    def guarda_participante(self):
        nombre = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_nombre.text()
        pais = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_pais.text()
        if Participantes.participanteExiste(nombre,pais):
            return QMessageBox.information(None, "Error", "El participante ya existe.")
        genero = self.ui_Main.admin_stackedWidget_combobox_pageParticipante_genero.currentText()
        edad = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_edad.text()
        deporte = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_deporte.text()
        Participantes.registrarParticipantes(nombre,pais,deporte,edad,genero)
        QMessageBox.information(None, "Éxito", "Participante guardado correctamente.")
    def elimina_participante(self):
        nombre = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_nombre.text()
        pais = self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_pais.text()
        if Participantes.eliminarParticipante(nombre, pais):
            QMessageBox.information(None, "Éxito", "Se eliminó el participante con Éxito")
            self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_nombre.clear()
            self.ui_Main.admin_stacketWidget_pageParticipante_lineEdit_pais.clear()
        else:
            QMessageBox.information(None, "Error", "No se encontró al participante.")
    def busca_participante(self,modo):
        lineEdit_nombre = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_lineEdit_nombre")
        lineEdit_pais = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_lineEdit_pais")
        lineEdit_deporte = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_lineEdit_deporte")
        tabla = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_table")
        #Consigue el nombre y pais escritos
        nombre = lineEdit_nombre.text()
        pais = lineEdit_pais.text()
        deporte = lineEdit_deporte.text()
        #Vaciar tabla
        tabla.setRowCount(0)
        #Buscar
        busqueda = Participantes.buscar_participante(nombre.upper(),pais.upper(),deporte.upper())
        #Si no se encuentra
        if not busqueda:
            tabla.setRowCount(0)
            return QMessageBox.information(None, "Error", "El participante no existe")
        #LLenar la tabla con los resultados
        for i in range(len(busqueda)):
            tabla.insertRow(i)
            for j in range(5):
                item = QTableWidgetItem(str(busqueda[i][j]))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                tabla.setItem(i, j, item)

    def seleccion_Cambiada_Admin(self):
        seleccion = self.ui_Main.admin_combobox_filtrarPor.currentText()  # Obtener el texto seleccionado
        if seleccion == "Atleta":
            self.ui_Main.admin_stackedWidged_secundary.setCurrentWidget(self.ui_Main.admin_stacketWidget_page_participante)
        if seleccion == "Pais":
            self.ui_Main.admin_stackedWidged_secundary.setCurrentWidget(self.ui_Main.admin_stacketWidget_page_pais)
        if seleccion == "Deporte":
            self.ui_Main.admin_stackedWidged_secundary.setCurrentWidget(self.ui_Main.admin_stacketWidget_page_deporte)

    def eventFilter(self, obj, event):
        if obj == self.ui_Main.admin_stacketWidget_pagePais_lineEdit_deportes:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.abrirVentanaDeportes()
                return True
        if obj == self.ui_Main.admin_stacketWidget_pageDeporte_lineEdit_paises:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.abrirVentanaPaises()
                return True
        if obj in (self.frame_superior_main, self.frame_superior_inicioSesion):
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.clickPosition = event.globalPosition()
                return True
            elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                delta = event.globalPosition() - self.clickPosition
                ventana = self.ui_Main if obj == self.frame_superior_main else self.ui_inicioSesion
                ventana.move(ventana.pos() + delta.toPoint())
                self.clickPosition = event.globalPosition()
                return True
        return False

    def show(self): 
        self.ui_inicioSesion.show()

#Interfaz grafica                

    def control_bt_minimizar(self,ventana):
        ventana.showMinimized()

    def control_bt_normal(self):
        self.ui_Main.showNormal()
        self.ui_Main.btn_Restaurar.hide()
        self.ui_Main.btn_Maximizar.show()

    def control_bt_maximizar(self):
        self.ui_Main.showMaximized()
        self.ui_Main.btn_Maximizar.hide()
        self.ui_Main.btn_Restaurar.show()


    def close_Program(self,ventana):
        # Crear un QMessageBox personalizado
        custom_box = QMessageBox()
        custom_box.setWindowTitle("Confirmar")
        custom_box.setText("¿Está seguro de Cerrar el programa?")
        custom_box.setStyleSheet("QLabel{ color : black; }")
        custom_box.setStyleSheet("background-color: white;")
        custom_box.setIcon(QMessageBox.Question)

        # Añadir botones personalizados
        yes_button = QPushButton("Sí")
        no_button = QPushButton("No")
        custom_box.addButton(yes_button, QMessageBox.YesRole)
        custom_box.addButton(no_button, QMessageBox.NoRole)

        # Conectar los botones a las funciones correspondientes
        yes_button.clicked.connect(lambda: self.close_App(True,ventana))
        no_button.clicked.connect(lambda: self.close_App(False,ventana))
        # Mostrar el cuadro de diálogo personalizado
        custom_box.exec()
    def close_App(self,confirmar,ventana):
        if confirmar:
            ventana.close()

class VentanaDeportes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ingresar deportes")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.boton_aceptar = QPushButton("Aceptar")

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.boton_aceptar)
        self.setLayout(self.layout)

        self.boton_aceptar.clicked.connect(self.accept)

    def obtenerTexto(self):
        return self.text_edit.toPlainText()
    
class VentanaPaises(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ingresar paises")
        self.setMinimumSize(300, 200)

        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.boton_aceptar = QPushButton("Aceptar")

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.boton_aceptar)
        self.setLayout(self.layout)

        self.boton_aceptar.clicked.connect(self.accept)

    def obtenerTexto(self):
        return self.text_edit.toPlainText()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiApp()
    ventana.show()
    sys.exit(app.exec())







    