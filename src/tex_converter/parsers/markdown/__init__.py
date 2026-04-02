"""
Parser Markdown modulare.

Architettura modulare per separare la sintassi vanilla da quella delle estensioni:
- `standard.py`: Markdown vanilla CommonMark (Phase 1 - completato)
- `pandoc.py`: Estensioni Pandoc (Phase 2 - pianificato)
- `html.py`: Estensioni HTML tag (Phase 2 - pianificato)
"""

from .standard import MarkdownParser, ParseInline, MakeParagraph

__all__: list[str] = ["MarkdownParser", "ParseInline", "MakeParagraph"]
