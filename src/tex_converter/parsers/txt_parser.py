import chardet
from typing import List
from ..model.document import Document, Block
from ..model.blocks import Paragraph


def TxtParser(path: str) -> Document:
    """Funzione per analizzare un file di testo e convertirlo in un documento LaTeX.
    Ogni riga del file di testo viene considerata un paragrafo separato.
    Args:
        path (str): Il percorso del file di testo da analizzare.
    Returns:
        Document: Il documento LaTeX.
    """
    # Rileva l'encoding del file di testo atraverso chardet
    with open(path, "rb") as f:
        RawData: bytes = f.read()
        detected: chardet.DetectionDict = chardet.detect(RawData)
        encoding: str = (
            detected.get("encoding") or "utf-8"
        )  # Fallback a UTF-8 se non viene rilevata l'encoding
        confidence: float = detected.get("confidence", 0)
        print(f"Encoding rilevato: {encoding} (confidence: {confidence})")

    # Se l'encoding è UTF-8, usiamo 'utf-8-sig' per gestire eventuali BOM
    if encoding.lower() in ("utf-8", "utf-8-sig"):
        encoding = "utf-8-sig"

    blocks: List[Block] = []

    with open(path, "r", encoding=encoding) as f:
        for line in f:
            line: str = line.strip()
            line = line.lstrip("\ufeff")  # Rimuove eventuali BOM residui

            if line:
                blocks.append(Paragraph(text=line))

    return Document(blocks=blocks)
