from dataclasses import dataclass
from typing import List, Union
from .blocks import (
    Paragraph,
    Heading,
    Image,
    Formula,
    ListBlock,
    ListItem,
    CodeBlock,
    BlockQuote,
    HorizontalRule,
    HtmlBlock,
    Table,
    TableRow,
    TableCell,
    Text,
)

Block = Union[
    Paragraph,
    Heading,
    Image,
    Formula,
    ListBlock,
    ListItem,
    CodeBlock,
    BlockQuote,
    HorizontalRule,
    HtmlBlock,
    Table,
    TableRow,
    TableCell,
    Text,
]


@dataclass
class Document:
    """Rappresenta un documento LaTeX composto da vari blocchi."""

    blocks: List[Block]
