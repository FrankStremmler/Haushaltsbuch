import sys
import traceback
import os
from dotenv import load_dotenv
# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# try:
from PySide6.QtWidgets import QApplication
# Importieren Sie das Fenster genau so, wie es bei Ihrem Einzeltest funktionierte
from views.main_window import MainWindow
from models.database import BudgetModel
from controllers.main_controller import MainController
# except ImportError as e:
#     print(f"Abbruch: Ein Modul konnte nicht geladen werden.\nDetails: {e}")
#     sys.exit(1)


def main():
    # Schützt vor Abstürzen während der Qt-Initialisierung
    try:
        app = QApplication(sys.argv)

        # Komponenten instanziieren
        model = BudgetModel("haushaltsbuch.db")
        view = MainWindow()
        controller = MainController(model, view)

        # Fenster anzeigen
        view.show()

        print("QApplication erfolgreich gestartet. Rufe app.exec() auf...")
        sys.exit(app.exec())

    except Exception as general_error:
        print("\n!!! KRITISCHER LAUFZEITFEHLER BEIM START DER GUI !!!")
        traceback.print_exc() # Erzwingt die Ausgabe des echten Fehlers im Terminal
        sys.exit(1)

if __name__ == "__main__":
    main()
