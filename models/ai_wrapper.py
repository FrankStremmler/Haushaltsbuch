# models/ai_wrapper.py
import json
from google import genai
from google.genai import types
from models.normalizer_models import NormalizedReceipt, NormalizedStatementPosition
from typing import List

class AIPlatformWrapper:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        if self.provider == "gemini":
            # Initialisiert den Google Client (Nutzt GEMINI_API_KEY aus der Umgebung)
            self.client = genai.Client()

    def analyze_receipt(self, file_path: str, mime_type: str) -> NormalizedReceipt:
        """
        Sendet ein Bild/PDF an die KI und garantiert die Rückgabe
        eines normalisierten NormalizedReceipt-Objekts.
        """
        if self.provider == "gemini":
            return self._analyze_receipt_with_gemini(file_path, mime_type)
        elif self.provider == "openai":
            return self._analyze_receipt_with_openai(file_path, mime_type)
        else:
            raise ValueError(f"Provider '{self.provider}' wird nicht unterstützt.")

    def _analyze_receipt_with_gemini(self, file_path: str, mime_type: str) -> NormalizedReceipt:
        # 1. Datei über die offizielle GenAI Files API hochladen
        with open(file_path, "rb") as f:
            uploaded_file = self.client.files.upload(
                file=f,
                config=types.UploadFileConfig(mime_type=mime_type)
            )

        prompt = "Analysiere diesen Beleg hochpräzise und extrahiere alle Daten."

        # 2. Structured Output erzwingen
        response = self.client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[uploaded_file, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=NormalizedReceipt, # Hier koppeln wir das normalisierte Pydantic-Modell
                temperature=0.1
            ),
        )

        # Datei aufräumen
        self.client.files.delete(name=uploaded_file.name)

        # 3. Validieren und als Python-Objekt zurückgeben
        return NormalizedReceipt.model_validate_json(response.text)

    def _analyze_receipt_with_openai(self, file_path: str, mime_type: str) -> NormalizedReceipt:
        """
        Platzhalter: Falls Sie später zu OpenAI GPT-4o wechseln,
        mappt diese Methode die OpenAI-Response auf das identische Pydantic-Modell.
        """
        # Hier würde der OpenAI API Call stehen (z.B. client.beta.chat.completions.parse)
        # Am Ende wird ebenfalls ein NormalizedReceipt-Objekt zurückgegeben.
        pass
