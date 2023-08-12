from datetime import datetime
import sys
import serial
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot



class GroundStationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ground Station")
        
        icon = QIcon('logo_cansat.ico')  # Reemplaza 'icon.ico' con la ruta de nuestra imagen
        
        # Establecer el ícono para la ventana
        self.setWindowIcon(icon)
        
        self.titulo_label = QLabel("Ground Station IITA Salta")
        self.titulo_label.setAlignment(Qt.AlignCenter)
        
        logo = QPixmap('logo2_cansat.png').scaled(250, 250, Qt.KeepAspectRatio)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        
        layout = QVBoxLayout()

        layout.addWidget(self.titulo_label)
        layout.addWidget(logo_label)
        
        
        self.packet_number_label = QLabel("Nro. de Paquete: ")
        self.base_pressure_label = QLabel("Presion Base: ")
        self.absolute_pressure_label = QLabel("Presion Absoluta: ")
        self.altitude_label = QLabel("Altitud: ")
        self.temperature_label = QLabel("Temperatura: ")
        self.magneX_label = QLabel("Magnetismo eje X: ")
        self.magneY_label = QLabel("Magnetismo eje Y: ")
        self.magneZ_label = QLabel("Magnetismo eje Z: ")
        
        
        # Aplicar formato visual a los QLabel
        self.titulo_label.setStyleSheet("font-size: 18px; font-weight: OCR A Extended; color: black;")
        self.packet_number_label.setStyleSheet("font-size: 14px; font-weight: bold; color: bold;")
        self.base_pressure_label.setStyleSheet("font-size: 14px; font-weight: bold; color: blue;")
        self.absolute_pressure_label.setStyleSheet("font-size: 14px; font-weight: bold; color: blue ")
        self.altitude_label.setStyleSheet("font-size: 14px; font-weight: bold; color: orange;")
        self.temperature_label.setStyleSheet("font-size: 14px; font-weight: bold; color: red;")
        self.magneX_label.setStyleSheet("font-size: 14px; font-weight: bold; color: purple;")
        self.magneY_label.setStyleSheet("font-size: 14px; font-weight: bold; color: purple;")
        self.magneZ_label.setStyleSheet("font-size: 14px; font-weight: bold; color: purple;")

        layout = QGridLayout()  # Cambiar a QGridLayout

        # Agregar los QLabel al diseño de la ventana
        layout.addWidget(self.titulo_label, 0, 0, 1, 2)  # Combina dos celdas en la primera fila
        layout.addWidget(logo_label, 0, 2, 1, 1)  # Ubica el logo en la tercera celda de la primera fila
        layout.addWidget(self.packet_number_label, 1, 0, 1, 2)  # Combina dos celdas en la segunda fila
        layout.addWidget(self.base_pressure_label, 1, 2)  # Ubica la etiqueta de presión base en la tercera celda de la segunda fila
        layout.addWidget(self.absolute_pressure_label, 1, 3)  # Ubica la etiqueta de presión absoluta en la cuarta celda de la segunda fila
        layout.addWidget(self.altitude_label, 2, 0, 1, 2)  # Combina dos celdas en la tercera fila
        layout.addWidget(self.temperature_label, 2, 2, 1, 2)  # Combina dos celdas en la tercera fila
        layout.addWidget(self.magneX_label, 3, 0, 1, 2)  # Combina dos celdas en la cuarta fila
        layout.addWidget(self.magneY_label, 3, 2, 1, 2)  # Combina dos celdas en la cuarta fila
        layout.addWidget(self.magneZ_label, 3, 3, 1, 2)  # Combina dos celdas en la quinta fila

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a SerialReaderThread instance
        self.serial_thread = SerialReaderThread("COM4")
        # Connect the data_received signal to the update_data slot
        self.serial_thread.data_received.connect(self.update_data)
        # Start the serial thread
        self.serial_thread.start()
        
        # Obtener la fecha actual
        now = datetime.now()
        self.file_name = "Telemetria/MAGNET-IITA_descriptivo_" + now.strftime("%Y_%m_%d_%H_%M") + ".txt"

        # Abrir un archivo de texto para escritura
        self.file = open(self.file_name, "w", encoding="utf-8")
        
        # Obtener la fecha actual
        now = datetime.now()
        self.file_name_analisis = "Telemetria/MAGNET-IITA_analisis_" + now.strftime("%Y_%m_%d_%H_%M") + ".txt"

        # Abrir un archivo de texto para escritura
        self.file_analisis = open(self.file_name_analisis, "w", encoding="utf-8")

    @pyqtSlot(str, str, str, str, str, str, str, str)
    def update_data(self, packet_number, base_pressure, absolute_pressure, altitude, temperature, magnex, magney, magnez):
        self.packet_number_label.setText(
    f""" ----------------------
| Nro. de Paquete | 
|{packet_number:^28}|
 ----------------------""")

        self.base_pressure_label.setText(
    f""" -------------------------
|     Presion Base        |
| {base_pressure + " Pa":^25} |
 -------------------------""")
        
        self.absolute_pressure_label.setText(
    f""" -------------------------
| Presion Absoluta     |
| {absolute_pressure + " Pa":^25} |
 -------------------------""")

        self.altitude_label.setText(
    f""" --------------------
| Altitud                     |
| {altitude + " m.s.n.m":<20}|
  --------------------""")

        self.temperature_label.setText(
    f""" ----------------------
| Temperatura         | 
| {temperature + ' °C' :25} |
 ----------------------""")
        
        self.magneX_label.setText(
    f""" ------------------------
| Magnetismo eje X   | 
| {magnex + ' µT' :^25} |
 ------------------------""")
        
        self.magneY_label.setText(
    f""" ------------------------
| Magnetismo eje Y   | 
| {magney + ' µT' :^25} |
 ------------------------""")
        
        self.magneZ_label.setText(
    f""" -----------------------
| Magnetismo eje Z   | 
| {magnez + ' µT' :^25} |
 -----------------------""")
        
        
        # Escribir los datos en el archivo
        self.file.write(f"Packet Number: {packet_number}\n")
        self.file.write(f"Base Pressure: {base_pressure} Pa\n")
        self.file.write(f"Absolute Pressure: {absolute_pressure} Pa\n")
        self.file.write(f"Altitude: {altitude} M.s.n.m\n")
        self.file.write(f"Temperature: {temperature} °C\n")
        self.file.write(f"Magnetismo en X: {magnex} µT\n")
        self.file.write(f"Magnetismo en Y: {magney} µT\n")
        self.file.write(f"Magnetismo en Z: {magnez} µT\n\n")
        
        # Escribir los datos en el archivo en el formato especificado
        data_line = f"{packet_number},{base_pressure},{absolute_pressure},{altitude},{temperature},{magnex},{magney},{magnez}\n"
        self.file_analisis.write(data_line)

    def closeEvent(self, event):
        # Cerrar el archivo al salir de la aplicación
        self.file.close()
        self.file_analisis.close()
        super().closeEvent(event)
    
        
        

class SerialReaderThread(QThread):
    data_received = pyqtSignal(str, str, str, str, str, str, str, str)

    def __init__(self, port, baud_rate=115200):
        super().__init__()
        self.serial_port = serial.Serial(port, baud_rate)

    def run(self):
        
        while True:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                print(data)
                values = data.split(",")
                if len(values) == 8:
                    packet_number = values[0]
                    base_pressure = values[1]
                    absolute_pressure = values[2]
                    altitude = values[3]
                    temperature = values[4]
                    magnex = values[5]
                    magney = values[6]
                    magnez = values[7]
                    self.data_received.emit(packet_number, base_pressure, absolute_pressure, altitude, temperature, magnex, magney, magnez)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroundStationWindow()
    window.showMaximized()
    sys.exit(app.exec())
