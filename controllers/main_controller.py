# controllers/main_controller.py
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QApplication
from views.settings_dialog import SettingsDialog
from views.style_helper import apply_global_theme
from models.config_model import ConfigManager

from models.ai_wrapper import AIPlatformWrapper

class AnalysisWorker(QThread):
    # Signals, um Daten sicher an den GUI-Hauptthread zu übergeben
    finished = Signal(object)  # Übergibt das fertige NormalizedReceipt-Objekt
    error = Signal(str)

    def __init__(self, file_path: str, mime_type: str):
        super().__init__()
        self.file_path = file_path
        self.mime_type = mime_type
        self.wrapper = AIPlatformWrapper(provider="gemini")

    def run(self):
        try:
            # KI-Analyse startet im Hintergrund-Thread
            normalized_data = self.wrapper.analyze_receipt(self.file_path, self.mime_type)
            self.finished.emit(normalized_data)
        except Exception as e:
            self.error.emit(str(e))

# In Ihrem MainController binden Sie das dann so an:
class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.config_manager = ConfigManager()
        self.view.btn_load.clicked.connect(self.start_receipt_analysis)
        # Event: Zahnrad-Button im Hauptfenster öffnet die Einstellungen
        self.view.btn_settings.clicked.connect(self.open_settings)

    def open_settings(self):
        # Dialog initialisieren (self.view als Parent für korrekte Zentrierung)
        dialog = SettingsDialog(self.view)

        # .exec() startet den modalen Loop. Gibt True zurück, wenn 'OK' geklickt wurde
        if dialog.exec():
            # Daten aus der View holen
            new_settings = dialog.get_selected_settings()

            # 1. KI-Provider im Config-Model aktualisieren
            self.config_manager.config.ai_provider = new_settings["ai_provider"]

            # 2. Theme im Config-Model aktualisieren & speichern
            self.config_manager.set_theme(new_settings["theme"])

            # 3. Live-Update: Das Stylesheet sofort auf die aktive App anwenden!
            apply_global_theme(QApplication.instance())

            print("Einstellungen erfolgreich gespeichert und Theme live aktualisiert.")

    def start_receipt_analysis(self):
        # Datei aus GUI wählen (z.B. über QFileDialog)
        file_path = "rewe_bon.pdf"
        mime_type = "application/pdf"

        # UI in Lade-Zustand versetzen
        self.view.set_loading(True)

        # Thread starten
        self.worker = AnalysisWorker(file_path, mime_type)
        self.worker.finished.connect(self.on_analysis_success)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_success(self, normalized_receipt):
        self.view.set_loading(False)

        # Das normalisierte JSON/Objekt geht direkt an das Datenbank-Model zur Speicherung
        # Die DB-Klasse weiß dank Pydantic exakt, welche Felder existieren (.merchant, .total_sum etc.)
        self.model.save_receipt_to_db(normalized_receipt)

        # UI aktualisieren
        self.view.refresh_ui()

    def on_analysis_error(self, error_msg):
        self.view.set_loading(False)
        self.view.show_error_message(error_msg)
