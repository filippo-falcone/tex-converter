import chardet
from typing import List
from ..model.document import Document, Block
from ..model.blocks import Paragraph, Heading, ListBlock


def MarkdownParser(path: str) -> Document:
    """Funzione per analizzare un file Markdown e convertirlo in un documento LaTeX.
    Args:
        path (str): Il percorso del file Markdown da analizzare.
    Returns:
        Document: Il documento LaTeX.
    """

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

    with open(path, "r", encoding=encoding) as f:
        lines: List[str] = f.readlines()

    blocks: List[Block] = []
    ListBuffer: List[str] = []
    ordered: bool = False
    i: int = 0

    while i < len(lines):
        line: str = lines[i].strip()
        line = line.lstrip("\ufeff")  # Rimuove eventuali BOM residui

        # Heading semplice: # Heading 1, ## Heading 2, ### Heading 3, etc.
        if line.startswith("#"):
            level: int = len(line) - len(line.lstrip("#"))
            heading_text: str = line.lstrip("#").strip()
            blocks.append(Heading(level=level, text=heading_text))
            i += 1
            continue

        # Liste non ordinate: - item
        if line.startswith("- "):
            ListBuffer.append(line[2:].strip())
            i += 1

            if i == len(lines) or not lines[i].strip().startswith("- "):
                blocks.append(ListBlock(items=ListBuffer, ordered=ordered))
                ListBuffer = []
            continue

        # Paragrafo normale
        if line:
            blocks.append(Paragraph(text=line))
        i += 1

    return Document(blocks=blocks)
