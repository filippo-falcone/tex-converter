import os
from .parsers.txt_parser import TxtParser
from .generators.latex_generator import LatexGenerator
from .model.document import Document


def Convert(InputPath: str, OutputPath: str) -> None:
    """Funzione principale per convertire un file di testo in un documento LaTeX.
    Args:
        InputPath (str): Il percorso del file di testo da convertire.
        OutputPath (str): Il percorso del file LaTeX da generare.
    """
    ext: str = os.path.splitext(InputPath)[1].lower()

    match ext:
        case ".txt":
            document: Document = TxtParser(InputPath)

        case _:
            raise ValueError(f"Unsupported file format: {ext}")

    LatexCode: str = LatexGenerator(document)

    with open(OutputPath, "w", encoding="utf-8") as f:
        f.write(LatexCode)
