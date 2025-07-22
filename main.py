import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtUiTools import *
from Usuarios import *
from Paises import Paises
from Lista_Doblemente_Enlazada import *
import Diccionario_Participantes as Participantes
import Backend_Sesion as backend_sesion
class MiApp(QObject):
    def __init__(self):
        
        super().__init__()
        loader = QUiLoader()
        file = QFile("diseño_olimpicos.ui")
        file.open(QFile.ReadOnly)
        self.ui_Main = loader.load(file)
        file.close()
        file2 = QFile("diseño_inicioSesion.ui")
        file2.open(QFile.ReadOnly)
        self.ui_inicioSesion = loader.load(file2)
        file2.close()

        # Crear una lista doblemente enlazada (en memoria)
        self.lista_paises = ListaDoblementeEnlazada()
        #Configura paises y usuarios
        self.objPais = Paises.Paises()
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
        nombre_pais = lineEdit_pais.text()
        if not self.objPais.paisExiste(nombre_pais):
            tabla.setRowCount(0)
            return QMessageBox.information(None, "Error", "El país no existe")
        infoPais = self.objPais.mostrar_pais(nombre_pais)
        #Añade info a la tabla respectiva
        row_position = tabla.rowCount()
        if row_position<1:
            tabla.insertRow(row_position)
        for i in range(3):
            item = QTableWidgetItem(str(infoPais[i]))
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            tabla.setItem(0, i, item)
        


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
        if Participantes.eliminarDeBase(nombre,pais):
            QMessageBox.information(None, "Éxito", "Se eliminó el participante con Exito")
        else:
            QMessageBox.information(None, "Error", "No se encontró al participante.")
    def busca_participante(self,modo):
        lineEdit_nombre = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_lineEdit_nombre")
        lineEdit_pais = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_lineEdit_pais")
        tabla = getattr(self.ui_Main, f"{modo}_stacketWidget_pageParticipante_table")
        nombre = lineEdit_nombre.text()
        pais = lineEdit_pais.text()
        if not Participantes.participanteExiste(nombre,pais):
            tabla.setRowCount(0)
            return QMessageBox.information(None, "Error", "El participante no existe")
        infoParticipante = Participantes.mostrar_participante(nombre,pais)
        #Añade info a la tabla respectiva
        row_position = tabla.rowCount()
        if row_position<1:
            tabla.insertRow(row_position)
        for i in range(5):
            item = QTableWidgetItem(str(infoParticipante[i]))
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            tabla.setItem(0, i, item)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiApp()
    ventana.show()
    sys.exit(app.exec())







    