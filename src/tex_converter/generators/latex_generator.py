from typing import List, Literal, LiteralString
from ..model.document import Document
from ..model.blocks import (
    Block,
    Paragraph,
    Heading,
    Image,
    Formula,
    ListBlock,
    ListItem,
    TaskList,
    TaskItem,
    CodeBlock,
    Blockquote,
    HorizontalRule,
    HtmlBlock,
    HtmlComment,
    Table,
    TableRow,
    TableCell,
    Text,
    Bold,
    Italic,
    Strikethrough,
    CodeInline,
    Link,
    ImageInline,
    MathInline,
    HtmlInline,
    LineBreak,
    Inline,
)
from ..utils import EscapeLatex, EscapeLatexUrl


# ============================================================
# INLINE → LATEX
# ============================================================
def InlineToLatex(inlines: List[Inline]) -> str:
    """Funzione ricorsiva che converte una lista di elementi inline in una stringa LaTeX. Gestisce diversi tipi di inline come testo, grassetto, corsivo, link e formule matematiche.
    Args:
        inlines (List[Inline]): La lista di elementi inline da convertire.
    Returns:
        str: La rappresentazione in LaTeX degli elementi inline.
    Raises:
        ValueError: Se viene fornito un tipo di inline non supportato."""
    out = []

    for token in inlines:
        match token:

            # -------------------------
            # Text - ESCAPARE CARATTERI SPECIALI
            # -------------------------
            case Text(text=t):
                out.append(EscapeLatex(t))

            # -------------------------
            # Bold
            # -------------------------
            case Bold(children=children):
                out.append(r"\textbf{" + InlineToLatex(children) + "}")

            # -------------------------
            # Italic
            # -------------------------
            case Italic(children=children):
                out.append(r"\textit{" + InlineToLatex(children) + "}")

            # -------------------------
            # Strikethrough
            # -------------------------
            case Strikethrough(children=children):
                out.append(r"\sout{" + InlineToLatex(children) + "}")

            # -------------------------
            # Code inline - ESCAPARE CONSERVATIVAMENTE
            # -------------------------
            case CodeInline(code=c):
                escaped_code: str = c.replace("\\", r"\textbackslash{}")
                escaped_code = escaped_code.replace("{", r"\{")
                escaped_code = escaped_code.replace("}", r"\}")
                escaped_code = escaped_code.replace("_", r"\_")
                out.append(r"\texttt{" + escaped_code + "}")

            # -------------------------
            # Link
            # -------------------------
            case Link(children=children, url=url):
                label: str = InlineToLatex(children)
                escaped_url = EscapeLatexUrl(url)
                out.append(rf"\href{{{escaped_url}}}{{{label}}}")

            # -------------------------
            # Image inline
            # -------------------------
            case ImageInline(src=src, alt=alt):
                escaped_src: str = src.replace("_", r"\_") if "_" in src else src
                out.append(rf"\includegraphics[height=1em]{{{escaped_src}}}")

            # -------------------------
            # Math inline
            # -------------------------
            case MathInline(expr=e):
                out.append(f"${e}$")

            # -------------------------
            # HTML inline (ignored)
            # -------------------------
            case HtmlInline():
                out.append("")

            # -------------------------
            # Line break
            # -------------------------
            case LineBreak():
                out.append(r"\\")

            # -------------------------
            # Default
            # -------------------------
            case _:
                raise ValueError(f"Inline non gestito: {type(token)}")

    return "".join(out)


# ============================================================
# BLOCK → LATEX
# ============================================================
def BlockToLatex(block: Block) -> str:
    """Funzione ricorsiva che converte un blocco in LaTeX. Gestisce diversi tipi di blocchi come paragrafi, intestazioni, immagini, formule, liste e tabelle.
    Args:
        block (Block): Il blocco da convertire in LaTeX.
    Returns:
        str: La rappresentazione in LaTeX del blocco.
    Raises:
        ValueError: Se viene fornito un tipo di blocco non supportato.
    """
    match block:

        # -------------------------
        # Paragraph - TRIMMARE SPAZI
        # -------------------------
        case Paragraph():
            content = InlineToLatex(block.children).strip()
            if content:
                return content + "\n\n"
            return ""

        # -------------------------
        # Heading
        # -------------------------
        case Heading():
            content: str = InlineToLatex(block.children)
            match block.level:
                case 1:
                    return rf"\section*{{{content}}}" + "\n\n"
                case 2:
                    return rf"\subsection*{{{content}}}" + "\n\n"
                case 3:
                    return rf"\subsubsection*{{{content}}}" + "\n\n"
                case _:
                    return rf"\paragraph*{{{content}}}" + "\n\n"

        # -------------------------
        # Image block
        # -------------------------
        case Image():
            latex: List[str] = [r"{\centering"]
            latex.append(
                rf"\includegraphics[width=0.88\linewidth,keepaspectratio]{{{block.path}}}"
            )
            if block.caption:
                latex.append(r"")
                latex.append(rf"{{\small {EscapeLatex(block.caption)}}}")
            latex.append(r"\par}")
            return "\n".join(latex) + "\n\n"

        # -------------------------
        # Formula
        # -------------------------
        case Formula():
            if block.display:
                return f"$${block.latex}$$\n\n"
            else:
                return f"${block.latex}$\n"

        # -------------------------
        # Code block
        # -------------------------
        case CodeBlock():
            return (
                rf"\begin{{verbatim}}"
                + "\n"
                + block.code
                + "\n"
                + rf"\end{{verbatim}}"
                + "\n\n"
            )

        # -------------------------
        # Blockquote
        # -------------------------
        case Blockquote():
            inner_lines = []
            for b in block.children:
                inner = BlockToLatex(b).strip()
                if inner:
                    inner_lines.append(inner)
            inner: str = "\n".join(inner_lines)
            return (
                rf"\begin{{quote}}" + "\n" + inner + "\n" + rf"\end{{quote}}" + "\n\n"
            )

        # -------------------------
        # Horizontal rule
        # -------------------------
        case HorizontalRule():
            return r"\noindent\rule{\textwidth}{0.5pt}" + "\n\n"

        # -------------------------
        # HTML block
        # -------------------------
        case HtmlBlock():
            html_content: str = block.html.strip()
            if not html_content:
                return ""
            return (
                rf"\begin{{quote}}"
                + "\n"
                + EscapeLatex(html_content)
                + "\n"
                + rf"\end{{quote}}"
                + "\n\n"
            )

        # -------------------------
        # HTML comment (ignored)
        # -------------------------
        case HtmlComment():
            return ""

        # -------------------------
        # ListBlock
        # -------------------------
        case ListBlock():
            env: Literal["enumerate"] | Literal["itemize"] = (
                "enumerate" if block.ordered else "itemize"
            )
            out: List[str] = [rf"\begin{{{env}}}"]
            for item in block.items:
                item_lines = []
                for b in item.children:
                    item_content: str = BlockToLatex(b).strip()
                    if item_content:
                        item_lines.append(item_content)
                if item_lines:
                    out.append(rf"\item {' '.join(item_lines)}")
            out.append(rf"\end{{{env}}}")
            return "\n".join(out) + "\n\n"

        # -------------------------
        # Task list
        # -------------------------
        case TaskList():
            out: List[str] = [r"\begin{itemize}"]
            for item in block.items:
                checkbox: str = r"$\checkmark$" if item.checked else r"$\square$"
                item_lines = []
                for b in item.children:
                    item_content: str = BlockToLatex(b).strip()
                    if item_content:
                        item_lines.append(item_content)
                if item_lines:
                    out.append(rf"\item {checkbox} {' '.join(item_lines)}")
            out.append(r"\end{itemize}")
            return "\n".join(out) + "\n\n"

        # -------------------------
        # Table
        # -------------------------
        case Table():
            if block.header is None:
                if len(block.rows) == 0:
                    return ""  # Tabella vuota
                HeaderRow: TableRow = block.rows[0]
                DataRows: List[TableRow] = block.rows[1:]
            else:
                HeaderRow: TableRow = block.header
                DataRows: List[TableRow] = block.rows

            ncols: int = len(HeaderRow.cells)
            colspec: str = " | ".join(["l"] * ncols)

            out = [rf"\begin{{tabular}}{{{colspec}}}", r"\hline"]

            # Header
            HeaderCells: List[str] = [
                "{" + InlineToLatex(cell.children).strip() + "}"
                for cell in HeaderRow.cells
            ]
            out.append(" & ".join(HeaderCells) + r" \\")
            out.append(r"\hline")

            # Rows
            for row in DataRows:
                RowCells: List[str] = [
                    "\\makecell{" + InlineToLatex(cell.children).strip() + "}"
                    for cell in row.cells
                ]
                out.append(" & ".join(RowCells) + r" \\")

            out.append(r"\hline")
            out.append(r"\end{tabular}")
            out.append(r"\vspace{0.5\baselineskip}")

            return "\n".join(out) + "\n\n"

        # -------------------------
        # Default
        # -------------------------
        case _:
            raise ValueError(f"Tipo di blocco non gestito: {type(block)}")


# ============================================================
# DOCUMENT → LATEX
# ============================================================
def LatexGenerator(document: Document) -> str:
    """Funzione che converte un documento in una stringa LaTeX completa.
    Include l'intestazione del documento, la conversione di tutti i blocchi e la chiusura.

    Args:
        document (Document): Il documento da convertire in LaTeX.

    Returns:
        str: La rappresentazione in LaTeX del documento.
    """
    lines = []

    # ===================== PREAMBLE =====================
    lines.append(r"\documentclass[11pt,a4paper]{article}")
    lines.append(r"\usepackage[utf8]{inputenc}")
    lines.append(r"\usepackage[italian]{babel}")
    lines.append(r"\usepackage[T1]{fontenc}")
    lines.append(r"\usepackage{graphicx}")
    lines.append(r"\usepackage{amsmath}")
    lines.append(r"\usepackage{amssymb}")
    lines.append(r"\usepackage{hyperref}")
    lines.append(r"\usepackage{xcolor}")
    lines.append(r"\usepackage{listings}")
    lines.append(r"\usepackage{microtype}")
    lines.append(r"\usepackage{float}")
    lines.append(r"\usepackage{makecell}")
    lines.append(r"\usepackage[normalem]{ulem}")
    lines.append(r"\usepackage[margin=1in]{geometry}")
    lines.append(r"")

    lines.append(r"\lstset{")
    lines.append(r"  basicstyle=\ttfamily\small,")
    lines.append(r"  breaklines=true,")
    lines.append(r"  frame=shadowbox,")
    lines.append(r"  backgroundcolor=\color{lightgray!20},")
    lines.append(r"}")
    lines.append(r"")

    lines.append(r"\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}")
    lines.append(r"\begin{document}")
    lines.append(r"")

    # ===================== CONTENUTO =====================
    for block in document.blocks:
        latex_block: str = BlockToLatex(block)
        if latex_block.strip():  # Solo se non vuoto
            lines.append(latex_block)

    # ===================== FINE DOCUMENTO =====================
    lines.append(r"\end{document}")

    # Pulire righe vuote multiple consecutive
    result: LiteralString = "\n".join(lines)

    # Compattare righe vuote multiple
    while "\n\n\n" in result:
        result = result.replace("\n\n\n", "\n\n")

    return result
