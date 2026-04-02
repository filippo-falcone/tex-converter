from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from .blocks import Block


@dataclass
class Document:
    """Rappresenta un documento completo con metadata opzionale.

    Attributes:
        blocks: Lista di blocchi che compongono il documento
        metadata: Metadata opzionale (per Phase 3: tipo documento, title, author, etc.)
    """

    blocks: List[Block]
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def doc_type(self) -> str:
        """Ritorna il tipo di documento (paper, thesis, book, document)."""
        return self.metadata.get("type", "document")

    @property
    def title(self) -> Optional[str]:
        """Ritorna il titolo del documento se presente."""
        return self.metadata.get("title")

    @property
    def author(self) -> Optional[str]:
        """Ritorna l'autore del documento se presente."""
        return self.metadata.get("author")
