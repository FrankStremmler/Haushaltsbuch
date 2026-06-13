# models/database.py
import sqlite3

class BudgetModel:
    def __init__(self, db_path="haushaltsbuch.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Erstellt die SQLite-Datenbank und alle Tabellen, falls sie nicht existieren."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Sync-Status
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS SYNC_STATUS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datei_name TEXT NOT NULL,
                datei_typ TEXT CHECK(datei_typ IN ('RECEIPT', 'STATEMENT')) NOT NULL,
                verarbeitet_am DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT CHECK(status IN ('SUCCESS', 'ERROR')) NOT NULL,
                fehler_text TEXT
            )
        ''')

        # 2. Kategorien
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CATEGORY (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                beschreibung TEXT
            )
        ''')

        # 3. Kassenzettel (Receipt)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RECEIPT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merchant TEXT NOT NULL,
                datum DATE NOT NULL,
                total_sum REAL NOT NULL,
                datei_pfad TEXT,
                raw_json TEXT,
                status TEXT CHECK(status IN ('pending', 'booked', 'suspicious')) DEFAULT 'pending',
                sync_id INTEGER,
                FOREIGN KEY (sync_id) REFERENCES SYNC_STATUS(id) ON DELETE SET NULL
            )
        ''')

        # 4. Einzelposten (Items)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ITEMS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                category_id INTEGER,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (receipt_id) REFERENCES RECEIPT(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES CATEGORY(id) ON DELETE SET NULL
            )
        ''')

        # 5. Bank Kenndaten
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BANK (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blz TEXT,
                bic TEXT
            )
        ''')

        # 6. Bankkonto (Bank_Account)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BANK_ACCOUNT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank_id INTEGER NOT NULL,
                kontonummer TEXT,
                iban TEXT NOT NULL UNIQUE,
                inhaber TEXT,
                waehrung TEXT DEFAULT 'EUR',
                FOREIGN KEY (bank_id) REFERENCES BANK(id) ON DELETE RESTRICT
            )
        ''')

        # 7. Kopfdaten Kontoauszug (Bank_Statement)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BANK_STATEMENT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank_account_id INTEGER NOT NULL,
                zeitraum_von DATE,
                zeitraum_bis DATE,
                anfangsbestand REAL,
                endbestand REAL,
                sync_id INTEGER,
                FOREIGN KEY (bank_account_id) REFERENCES BANK_ACCOUNT(id) ON DELETE RESTRICT,
                FOREIGN KEY (sync_id) REFERENCES SYNC_STATUS(id) ON DELETE SET NULL
            )
        ''')

        # 8. Einzelne Posten auf dem Auszug (Bank_Statement_Position)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BANK_STATEMENT_POSITION (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bank_statement_id INTEGER NOT NULL,
                category_id INTEGER,
                matched_receipt_id INTEGER,
                buchungsdatum DATE NOT NULL,
                verwendungszweck TEXT,
                beguenstigter_auftraggeber TEXT,
                betrag REAL NOT NULL,
                FOREIGN KEY (bank_statement_id) REFERENCES BANK_STATEMENT(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES CATEGORY(id) ON DELETE SET NULL,
                FOREIGN KEY (matched_receipt_id) REFERENCES RECEIPT(id) ON DELETE SET NULL
            )
        ''')

        conn.commit()
        conn.close()

    def get_all_receipts(self):
        """Holt alle Belege aus der Datenbank für die GUI-Tabelle."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, merchant, datum, total_sum, status FROM RECEIPT ORDER BY datum DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
