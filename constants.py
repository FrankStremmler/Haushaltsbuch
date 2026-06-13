# constants.py
import os

# --- BASIS VERZEICHNISSE ---
# Ermittelt das Verzeichnis, in dem diese constants.py liegt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")

# --- DATEI-PFADE (GLOBAL) ---
DB_PATH = os.path.join(BASE_DIR, "haushaltsbuch.db")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# --- ICON-PFADE (Mit korrigiertem SVG-Namespace) ---
ANALYZE_ICON_PATH = os.path.join(ICONS_DIR, "analyze_icon.svg")
SETTINGS_ICON_PATH = os.path.join(ICONS_DIR, "settings_icon.svg")
HISTORY_ICON_PATH = os.path.join(ICONS_DIR, "history_icon.svg")
PIGGY_ICON_PATH = os.path.join(ICONS_DIR, "piggy_icon.svg")

# --- ZUSTÄNDE & STATI (State Machine) ---
STATUS_PENDING = "pending"
STATUS_BOOKED = "booked"
STATUS_SUSPICIOUS = "suspicious"

STATUS_SYNC_SUCCESS = "SUCCESS"
STATUS_SYNC_ERROR = "ERROR"

# --- KI PROVIDER ---
PROVIDER_GEMINI = "gemini"
PROVIDER_OPENAI = "openai"

# --- MIME-TYPES & DATEI-ENDUNGEN ---
MIME_PDF = "application/pdf"
MIME_JPEG = "image/jpeg"
MIME_PNG = "image/png"

SUPPORTED_EXTENSIONS = {
    "pdf": MIME_PDF,
    "jpg": MIME_JPEG,
    "jpeg": MIME_JPEG,
    "png": MIME_PNG
}
