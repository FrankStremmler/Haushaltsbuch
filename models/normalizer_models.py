# models/normalizer_models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class NormalizedItem(BaseModel):
    name: str = Field(..., description="Name des Artikels")
    price: float = Field(..., description="Preis des Artikels in Euro")
    category_proposal: Optional[str] = Field(None, description="Kategorievorschlag der KI")

class NormalizedReceipt(BaseModel):
    merchant: str = Field(..., description="Name des Händlers")
    date_booked: date = Field(..., description="Kaufdatum (YYYY-MM-DD)")
    total_sum: float = Field(..., description="Gesamtsumme des Belegs")
    items: List[NormalizedItem] = Field(default_factory=list)

class NormalizedStatementPosition(BaseModel):
    booking_date: date = Field(..., description="Buchungsdatum")
    purpose: str = Field(..., description="Verwendungszweck")
    partner: str = Field(..., description="Begünstigter oder Auftraggeber")
    amount: float = Field(..., description="Betrag (positiv oder negativ)")
    category_proposal: Optional[str] = Field(None, description="Kategorievorschlag für Direktbuchungen")
