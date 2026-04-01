from dataclasses import dataclass
from typing import List, Union
from .blocks import Paragraph, Heading, Image, Formula, ListBlock, Table

Block = Union[Paragraph, Heading, Image, Formula, ListBlock, Table]


@dataclass
class Document:
    """Rappresenta un documento LaTeX composto da vari blocchi."""

    blocks: List[Block]
