from typing import List
from ..model.document import Document, Block
from ..model.blocks import Paragraph


def parse_txt(path: str) -> Document:
    blocks: List[Block] = []

    with open(path, "r") as f:
        for line in f:
            line: str = line.strip()
            if line:
                blocks.append(Paragraph(text=line))

    return Document(blocks=blocks)
