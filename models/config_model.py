# models/config_model.py
import json
import os
from pydantic import BaseModel, Field

class ThemeColors(BaseModel):
    background: str = Field("#1e1e1e", description="Haupt-Hintergrundfarbe")
    surface: str = Field("#2d2d2d", description="Farbe für Karten, Tabellen, Sidebar")
    text: str = Field("#ffffff", description="Standard Textfarbe")
    accent: str = Field("#2563eb", description="Akzentfarbe für Buttons/Highlights")

class AppConfig(BaseModel):
    ai_provider: str = Field("gemini", description="Ausgewählter KI-Anbieter (gemini, openai)")
    current_theme: str = Field("dark", description="Aktuelles Farbschema-Name")
    theme: ThemeColors = Field(default_factory=ThemeColors)

class ConfigManager:
    _instance = None
    CONFIG_FILE = "config.json"

    def __new__(cls):
        """Singleton-Pattern: Es gibt anwendungsweit nur eine Konfiguration"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.config = AppConfig.model_validate_json(f.read())
            except Exception:
                self.config = AppConfig() # Fallback bei korrupter Datei
        else:
            self.config = AppConfig()
            self.save_config()

    def save_config(self):
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(self.config.model_dump_json(indent=4))

    def set_theme(self, theme_name: str):
        self.config.current_theme = theme_name
        if theme_name == "dark":
            self.config.theme = ThemeColors(background="#1e1e1e", surface="#2d2d2d", text="#ffffff", accent="#2563eb")
        elif theme_name == "light":
            self.config.theme = ThemeColors(background="#f8fafc", surface="#ffffff", text="#0f172a", accent="#3b82f6")
        self.save_config()


class AIPlatformWrapper:
    def __init__(self):
        # Holt sich den aktuell gespeicherten Provider (z.B. "gemini" oder "openai")
        self.config_manager = ConfigManager()
        self.update_provider()

    def update_provider(self):
        self.provider = self.config_manager.config.ai_provider.lower()
        if self.provider == "gemini":
            from google import genai
            self.client = genai.Client()
