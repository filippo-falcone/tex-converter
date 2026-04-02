import re
import chardet
from typing import List
from ..model.document import Document, Block
from ..model.blocks import (
    Paragraph,
    Heading,
    Image,
    Formula,
    ListBlock,
    ListItem,
    CodeBlock,
    Blockquote,
    HorizontalRule,
    HtmlBlock,
    Table,
    TableRow,
    TableCell,
    Text,
)


def MakeParagraph(text: str) -> Paragraph:
    """Funzione per creare un paragrafo da una stringa di testo.
    Args:
        text (str): Il testo da convertire in un paragrafo.
    Returns:
        Paragraph: Il paragrafo creato.
    """
    return Paragraph(children=[Text(text)])


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
            blocks.append(Heading(level=level, children=[Text(text=heading_text)]))
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

        # Liste ordinate: 1. item
        if re.match(r"\d+\.\s", line):
            item: str = re.sub(r"^\d+\.\s", "", line).strip()
            ListBuffer.append(item)
            ordered = True
            i += 1

            if i == len(lines) or not re.match(r"\d+\.\s", lines[i].strip()):
                blocks.append(ListBlock(items=ListBuffer, ordered=ordered))
                ListBuffer = []
            continue

        # Immagini: ![alt text](path)
        ImgMatch: re.Match[str] | None = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if ImgMatch:
            alt: str = ImgMatch.groups()[0]
            PathImg: str = ImgMatch.groups()[1]
            blocks.append(Image(path=PathImg, alt=alt, caption=alt))
            i += 1
            continue

        # Formule Display: $$formula$$
        if line.startswith("$$"):
            FormulaLines: List[str] = []
            i += 1

            # Raccogli tutte le linee fino alla chiusura $$
            while i < len(lines) and not lines[i].strip().startswith("$$"):
                FormulaLines.append(lines[i])
                i += 1

            blocks.append(Formula(latex="\n".join(FormulaLines), display=True))
            i += 1  # Salta la linea di chiusura $$
            continue

        # Formule Inline: $formula$
        InlineFormula = re.findall(r"\$(.+?)\$", line)
        if InlineFormula:
            for formula in InlineFormula:
                blocks.append(Formula(latex=formula, display=False))
            i += 1
            continue

        # Blocchi di codice: ```language\ncode\n```
        if line.startswith("```"):
            language: str | None = line[3:].strip() or None
            CodeLines: List[str] = []
            i += 1

            # Raccogli tutte le linee fino alla chiusura ```
            while i < len(lines) and not lines[i].strip().startswith("```"):
                CodeLines.append(lines[i].rstrip("\n"))
                i += 1

            blocks.append(CodeBlock(language=language, code="\n".join(CodeLines)))
            i += 1  # Salta la linea di chiusura ```
            continue

        # Blockquote: > quote
        if line.startswith(">"):
            QuoteLines: List[str] = [line[1:].strip()]
            i += 1

            while i < len(lines) and lines[i].strip().startswith(">"):
                QuoteLines.append(lines[i].strip()[1:].strip())
                i += 1

            blocks.append(Blockquote(children=[MakeParagraph("\n".join(QuoteLines))]))
            continue

        # Horizontal Rule: --- o *** o ___
        if line in ("---", "***", "___"):
            blocks.append(HorizontalRule())
            i += 1
            continue

        # HTML: <tag>...</tag>
        if re.match(r"<[A-Za-z]+", line):
            HtmlLines: List[str] = [line]
            i += 1

            while i < len(lines) and not lines[i].strip().startswith("</"):
                HtmlLines.append(lines[i].rstrip("\n"))
                i += 1

            if i < len(lines):
                HtmlLines.append(lines[i].rstrip("\n"))
                i += 1

            blocks.append(HtmlBlock(html="\n".join(HtmlLines)))
            continue

        # Tabelle: | Header 1 | Header 2 |\n| --- | --- |\n| Cell 1 | Cell 2 |
        if "|" in line and re.match(r"\|.*\|", line):
            HeaderCells: List[TableCell] = [
                TableCell(children=[Text(c.strip())])
                for c in line.strip("|").split("|")
            ]
            header = TableRow(cells=HeaderCells)

            i += 1

            # Salta la riga di separazione (es. |---|---|)
            if i < len(lines) and re.match(r"\|[-: ]+\|", lines[i].strip()):
                i += 1

            rows: List[TableRow] = []
            while i < len(lines) and "|" in lines[i]:
                row_cells: List[TableCell] = [
                    TableCell(children=[Text(c.strip())])
                    for c in lines[i].strip().strip("|").split("|")
                ]
                rows.append(TableRow(cells=row_cells))
                i += 1

            blocks.append(Table(header=header, rows=rows))
            continue

        # Paragrafo normale
        if line:
            blocks.append(MakeParagraph(line))
        i += 1

    return Document(blocks=blocks)
