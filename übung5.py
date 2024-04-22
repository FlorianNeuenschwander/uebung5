import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDesktopServices, QAction
from PyQt5.QtCore import QUrl, QDate

class Fenster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.createLayout()
        self.createConnect()

    def createLayout(self):
        ## Fenstertitel / Layout
        self.setWindowTitle("GUI Programmierung")
        layout = QFormLayout()
        self.setMinimumSize(800,200)

        ## Zentrierung der Widgets
        center = QWidget()
        center.setLayout(layout)
        self.setCentralWidget(center)

        ## Widgets erstellen
        self.vorname = QLineEdit()
        self.nachname = QLineEdit()
        self.bday = QDateEdit()
        self.bday.setDisplayFormat("dd/MM/yyyy")
        self.adr = QLineEdit()
        self.plz = QLineEdit()
        self.ort = QLineEdit()
        self.land = QComboBox()
        self.land.addItems(["Schweiz", "Deutschland", "Österreich", "andere"])

        self.savek = QPushButton("Save")
        self.show_map_button = QPushButton("Auf Karte zeigen")
        self.load_button = QPushButton("Laden")

        ## Layout füllen
        layout.addRow("Vorname:", self.vorname)
        layout.addRow("Nachname:", self.nachname)
        layout.addRow("Geburtstag:", self.bday)
        layout.addRow("Adresse:", self.adr)
        layout.addRow("PLZ:", self.plz)
        layout.addRow("Ortschaft:", self.ort)
        layout.addRow("Land:", self.land)
        layout.addRow(self.savek)
        layout.addRow(self.show_map_button)
        layout.addRow(self.load_button)

        ## Menueleiste
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        viewmenu = menubar.addMenu("View")

        self.save = QAction("Save", self)
        self.quit = QAction("Quit", self)
        self.show_map_action = QAction("Karte anzeigen", self)
        self.load_action = QAction("Laden", self)

        filemenu.addAction(self.save)
        filemenu.addAction(self.quit)
        viewmenu.addAction(self.show_map_action)
        filemenu.addAction(self.load_action)

        ## Fenster anzeigen
        self.show()

    def createConnect(self):
        self.quit.triggered.connect(self.close)
        self.save.triggered.connect(self.speicher)
        self.savek.clicked.connect(self.speicher)
        self.show_map_action.triggered.connect(self.show_map)
        self.load_action.triggered.connect(self.load_data)
        self.load_button.clicked.connect(self.load_data)

        # Verknüpfe den Button-Click-Signal mit der Methode show_map
        self.show_map_button.clicked.connect(self.show_map)

    def closeEvent(self, event):
        event.accept()

    def speicher(self):
        filename, typ = QFileDialog.getSaveFileName(self, "Datei speichern",
                                                    "",
                                                    "Alle (*.*)")
        print(filename)

    def show_map(self):
        address = self.adr.text()
        plz = self.plz.text()
        ort = self.ort.text()
        land = self.land.currentText()

        map_url = f"https://www.google.com/maps/place/{address}+{plz}+{ort}+{land}"
        QDesktopServices.openUrl(QUrl(map_url))

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Datensatz laden", "", "Alle Dateien (*.*);;Textdateien (*.txt)")
        if filename:
            with open(filename, 'r') as file:
                lines = file.readlines()
                if len(lines) == 7:
                    self.vorname.setText(lines[0].strip())
                    self.nachname.setText(lines[1].strip())
                    self.bday.setDate(QDate.fromString(lines[2].strip(), "dd/MM/yyyy"))
                    self.adr.setText(lines[3].strip())
                    self.plz.setText(lines[4].strip())
                    self.ort.setText(lines[5].strip())
                    index = self.land.findText(lines[6].strip())
                    if index != -1:
                        self.land.setCurrentIndex(index)
                else:
                    QMessageBox.warning(self, "Fehler", "Ungültiges Dateiformat.")

def main():
    app = QApplication(sys.argv)  
    mainwindow = Fenster()       
    mainwindow.raise_()           
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()