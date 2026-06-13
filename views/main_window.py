# views/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QHeaderView
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication
import sys

import constants as const

SETTINGS_ICON_PATH = const.SETTINGS_ICON_PATH
ANALYZE_ICON_PATH = const.ANALYZE_ICON_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Hauptfenster-Konfiguration
        self.setWindowTitle("Intelligentes Haushaltsbuch")
        self.resize(800, 600)
        self.setWindowIcon(QIcon(ANALYZE_ICON_PATH)) # Haupt-Icon links oben

        # 2. Zentrales Basis-Widget setzen
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 3. Vertikales Hauptlayout für das Zentral-Widget
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # 4. Obere Menüleiste (Top Bar) erstellen
        self.top_bar = QHBoxLayout()

        # Großer Analyse-Button für Kassenzettel/PDFs
        self.btn_analyze = QPushButton(" Beleg analysieren")
        self.btn_analyze.setIcon(QIcon(ANALYZE_ICON_PATH))
        self.btn_analyze.setIconSize(QSize(20, 20))
        self.btn_analyze.setCursor(Qt.CursorShape.PointingHandCursor)

        # Einstellungs-Button (Zahnrad)
        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(QIcon(SETTINGS_ICON_PATH))
        self.btn_settings.setIconSize(QSize(20, 20))
        self.btn_settings.setFixedSize(36, 36)
        self.btn_settings.setToolTip("Einstellungen öffnen")
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)

        # Elemente in die Top-Bar packen
        self.top_bar.addWidget(self.btn_analyze)
        self.top_bar.addStretch()  # Schiebt das Zahnrad nach ganz rechts außen
        self.top_bar.addWidget(self.btn_settings)

        # Top-Bar dem Hauptlayout hinzufügen (Jetzt ist sie eingebunden!)
        self.main_layout.addLayout(self.top_bar)

        # 5. Datentabelle für Belege erstellen
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Händler", "Datum", "Gesamtsumme", "Status"])

        # Tabellen-Styling für bessere Lesbarkeit
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Tabelle dem Hauptlayout hinzufügen (Jetzt ist sie eingebunden!)
        self.main_layout.addWidget(self.table)

    def set_loading_state(self, is_loading: bool):
        """Sperrt die Buttons während des KI-Hintergrund-Calls"""
        if is_loading:
            self.btn_analyze.setText("Analysiere mit KI...")
            self.btn_analyze.setEnabled(False)
            self.btn_settings.setEnabled(False)
        else:
            self.btn_analyze.setText(" Beleg analysieren")
            self.btn_analyze.setEnabled(True)
            self.btn_settings.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()

    sys.exit(app.exec())
