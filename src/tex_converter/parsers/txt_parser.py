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
    blocks: List[Block] = []

    with open(path, "r") as f:
        for line in f:
            line: str = line.strip()
            if line:
                blocks.append(Paragraph(text=line))

    return Document(blocks=blocks)
