"""
Parser per diversi formati di input.

Ogni parser converte un file sorgente in un AST comune (Abstract Syntax Tree)
che può essere elaborato dal generatore LaTeX.

Formati supportati:
- TXT: File di testo semplice
- Markdown: Formato Markdown con architettura estensibile
- HTML: Documenti HTML (pianificato)
- DOCX: Documenti Microsoft Word (pianificato)
- PDF: Documenti PDF (pianificato)
"""

from .txt_parser import TxtParser
from .markdown import MarkdownParser

__all__ = ["TxtParser", "MarkdownParser"]
