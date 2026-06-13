# views/settings_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QDialogButtonBox, QLabel
from PySide6.QtGui import QIcon
from models.config_model import ConfigManager
import constants as const

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Einstellungen")
        self.setMinimumWidth(350)

        # Zahnrad-Icon über die globalen Konstanten laden
        self.setWindowIcon(QIcon(const.SETTINGS_ICON_PATH))

        # Konfiguration laden
        self.config_manager = ConfigManager()
        current_config = self.config_manager.config

        # Layouts aufbauen
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # 1. KI-Provider Auswahlfeld
        self.combo_provider = QComboBox()
        self.combo_provider.addItems([const.PROVIDER_GEMINI.capitalize(), const.PROVIDER_OPENAI.capitalize()])

        # Aktuellen Wert aus der config.json vorselektieren
        index_provider = self.combo_provider.findText(current_config.ai_provider.capitalize())
        if index_provider >= 0:
            self.combo_provider.setCurrentIndex(index_provider)

        # 2. Farbschema Auswahlfeld
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark", "Light"])

        # Aktuellen Wert aus der config.json vorselektieren
        index_theme = self.combo_theme.findText(current_config.current_theme.capitalize())
        if index_theme >= 0:
            self.combo_theme.setCurrentIndex(index_theme)

        # Zeilen zum Formular hinzufügen
        self.form_layout.addRow(QLabel("KI-Dienstleister:"), self.combo_provider)
        self.form_layout.addRow(QLabel("Farbschema:"), self.combo_theme)
        self.main_layout.addLayout(self.form_layout)

        # 3. Standard OK- und Abbrechen-Buttons von Qt
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)  # Schließt das Fenster bei OK
        self.button_box.rejected.connect(self.reject)  # Schließt das Fenster bei Abbrechen
        self.main_layout.addWidget(self.button_box)

    def get_selected_settings(self) -> dict:
        """Gibt die vom Nutzer gewählten Einstellungen an den Controller zurück."""
        return {
            "ai_provider": self.combo_provider.currentText().lower(),
            "theme": self.combo_theme.currentText().lower()
        }
