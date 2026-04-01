from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Paragraph:
    """Rappresenta un paragrafo in un documento LaTeX."""

    text: str


@dataclass
class Heading:
    """Rappresenta una intestazione in un documento LaTeX."""

    level: int
    text: str


@dataclass
class Image:
    """Rappresenta un'immagine in un documento LaTeX."""

    path: str
    caption: Optional[str] = None


@dataclass
class Formula:
    """Rappresenta una formula in un documento LaTeX. Può essere visualizzata in modalità inline o display."""

    latex: str
    display: bool = True


@dataclass
class ListBlock:
    """Rappresenta una lista in un documento LaTeX. Può essere ordinata o non ordinata."""

    items: List[str]
    ordered: bool = False


@dataclass
class Table:
    """Rappresenta una tabella in un documento LaTeX."""

    headers: List[str]
    rows: List[List[str]]
