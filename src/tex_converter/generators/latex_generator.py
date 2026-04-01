from typing import List, Literal
from ..model.document import Document
from ..model.blocks import Paragraph, Heading, Image, Formula, ListBlock, Table


def generate_latex(document: Document) -> str:
    """Genera il codice LaTeX a partire da un documento rappresentato come istanza di Document.
    Args:
        document (Document): Il documento da convertire in LaTeX.
    Returns:
        str: Il codice LaTeX generato.
    """
    lines: List[str] = []

    # Intestazione base LaTeX

    lines.append("\\documentclass{article}")
    lines.append("\\usepackage{graphicx}")
    lines.append("\\usepackage{amsmath}")
    lines.append("\\begin{document}")
    lines.append("")

    for block in document.blocks:
        match block:
            case Paragraph(text=t):
                lines.append(t)
                lines.append("")

            case Heading(level=l, text=t):
                if l == 1:
                    lines.append(f"\\section{{{t}}}")
                elif l == 2:
                    lines.append(f"\\subsection{{{t}}}")
                else:
                    lines.append(f"\\subsubsection{{{t}}}")
                lines.append("")

            case Image(path=p, caption=c):
                lines.append("\\begin{figure}[h]")
                lines.append("\\centering")
                lines.append(f"\\includegraphics[width=\\linewidth]{{{p}}}")
                if c:
                    lines.append(f"\\caption{{{c}}}")
                lines.append("\\end{figure}")
                lines.append("")

            case Formula(latex=fx, display=d):
                if d:
                    lines.append(f"\\[ {fx} \\]")
                else:
                    lines.append(f"${fx}$")
                lines.append("")

            case ListBlock(items=items, ordered=ord):
                env: Literal["enumerate"] | Literal["itemize"] = (
                    "enumerate" if ord else "itemize"
                )
                lines.append(f"\\begin{{{env}}}")
                for item in items:
                    lines.append(f"  \\item {item}")
                lines.append(f"\\end{{{env}}}")
                lines.append("")

            case Table(headers=h, rows=r):
                col_spec: str = " | ".join(["l"] * len(h))
                lines.append("\\begin{tabular}{" + col_spec + "}")
                lines.append(" \\hline")
                lines.append(" & ".join(h) + " \\\\")
                lines.append(" \\hline")
                for row in r:
                    lines.append(" & ".join(row) + " \\\\")
                lines.append(" \\hline")
                lines.append("\\end{tabular}")
                lines.append("")

            case _:
                raise ValueError(f"Tipo di blocco non gestito: {type(block)}")
    lines.append("\\end{document}")
    return "\n".join(lines)
