from dataclasses import dataclass
from typing import List, Optional

# =========================
# Classi base
# =========================


@dataclass
class Block:
    """Classe base astratta per tutti i blocchi di un documento (elementi a livello di paragrafo)."""

    pass


@dataclass
class Inline:
    """Classe base astratta per tutti gli elementi inline (dentro paragrafi, heading, celle, ecc.)."""

    pass


# =========================
# Elementi Inline
# =========================


@dataclass
class Text(Inline):
    """Rappresenta un testo semplice in un documento LaTeX."""

    text: str


@dataclass
class Bold(Inline):
    """Rappresenta un testo in grassetto in un documento LaTeX."""

    children: List[Inline]


@dataclass
class Italic(Inline):
    """Rappresenta un testo in corsivo in un documento LaTeX."""

    children: List[Inline]


@dataclass
class CodeInline(Inline):
    """Rappresenta un testo in stile codice in un documento LaTeX."""

    code: str


@dataclass
class Link(Inline):
    """Rappresenta un link in un documento LaTeX."""

    children: List[Inline]
    url: str


@dataclass
class ImageInline(Inline):
    """Rappresenta un'immagine inline in un documento LaTeX."""

    src: str
    alt: Optional[str] = None


@dataclass
class MathInline(Inline):
    """Rappresenta una formula matematica inline in un documento LaTeX."""

    expr: str


@dataclass
class HtmlInline(Inline):
    """Rappresenta un elemento HTML inline in un documento LaTeX."""

    html: str


# =========================
# Blocchi principali
# =========================


@dataclass
class Paragraph(Block):
    """Rappresenta un paragrafo in un documento LaTeX."""

    children: List[Inline]


@dataclass
class Heading(Block):
    """Rappresenta una intestazione in un documento LaTeX."""

    level: int
    children: List[Inline]


@dataclass
class Image(Block):
    """Rappresenta un'immagine in un documento LaTeX."""

    path: str
    alt: Optional[str] = None
    caption: Optional[str] = None


@dataclass
class Formula(Block):
    """Rappresenta una formula in un documento LaTeX. Può essere visualizzata in modalità inline o display."""

    latex: str
    display: bool = True


@dataclass
class CodeBlock(Block):
    """Rappresenta un blocco di codice in un documento LaTeX."""

    language: Optional[str]
    code: str


# =========================
# Liste
# =========================


@dataclass
class ListItem(Block):
    """Rappresenta un elemento di una lista in un documento LaTeX."""

    children: List[Block]


@dataclass
class ListBlock(Block):
    """Rappresenta una lista in un documento LaTeX. Può essere ordinata o non ordinata."""

    items: List[ListItem]
    ordered: bool = False


# =========================
# Tabelle
# =========================


@dataclass
class TableCell:
    """Rappresenta una cella di una tabella in un documento LaTeX."""

    children: List[Inline]


@dataclass
class TableRow:
    """Rappresenta una riga di una tabella in un documento LaTeX."""

    cells: List[TableCell]


@dataclass
class Table(Block):
    """Rappresenta una tabella in un documento LaTeX. Può avere intestazioni opzionali e un numero variabile di righe."""

    headers: Optional[TableRow]
    rows: List[TableRow]


# =========================
# Altri blocchi
# =========================


@dataclass
class Blockquote(Block):
    """Rappresenta un blocco di citazione in un documento LaTeX."""

    children: List[Block]


@dataclass
class HorizontalRule(Block):
    """Rappresenta una linea orizzontale in un documento LaTeX."""

    pass


@dataclass
class HtmlBlock(Block):
    """Rappresenta un blocco HTML in un documento LaTeX."""

    html: str
