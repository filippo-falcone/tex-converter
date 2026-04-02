from dataclasses import dataclass
from typing import List
from .blocks import Block


@dataclass
class Document:
    blocks: List[Block]
