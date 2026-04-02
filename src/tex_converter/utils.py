# ============================================================
# LATEX ESCAPER - Utility per escapare caratteri speciali
# ============================================================


def EscapeLatex(text: str) -> str:
    """Funzione per escapare caratteri speciali di LaTeX.
    Args:
        text (str): Il testo da escapare

    Returns:
        str: Il testo con caratteri escapati per LaTeX
    """

    text = text.replace("\\", r"\textbackslash{}")

    text = text.replace("{", r"\{")
    text = text.replace("}", r"\}")

    text = text.replace("#", r"\#")
    text = text.replace("$", r"\$")
    text = text.replace("&", r"\&")
    text = text.replace("%", r"\%")
    text = text.replace("_", r"\_")
    text = text.replace("^", r"\^{}")
    text = text.replace("~", r"\textasciitilde{}")

    return text


def EscapeLatexUrl(url: str) -> str:
    """Funzione per escapare URL per LaTeX (meno aggressivo che EscapeLatex).
    URL ha regole diverse - non escapare tutto.
    Solo escapare %, #, e altri che rompono href.

    Args:
        url (str): L'URL da escapare

    Returns:
        str: L'URL escapato per LaTeX
    """
    # In URL, principalmente escapare % e #
    url = url.replace("%", r"\%")
    url = url.replace("#", r"\#")
    return url
