"""
Modulo Markdown: contiene il parser per i documenti in formato Markdown. Al momento supporta solo la sintassi standard, ma in futuro potrebbe essere esteso per supportare estensioni come GitHub Flavored Markdown (GFM) o altre varianti. Il modulo è organizzato in più file per mantenere il codice pulito e modulare:
- `standard.py`: contiene il parser per la sintassi Markdown standard, che include intestazioni, paragrafi, liste, link, immagini, codice inline e blocchi di codice.
- `html.py`: conterrà il parser per le estensioni HTML, come i tag `<sup>`, `<sub>` e `<mark>`. Al momento è vuoto, ma sarà implementato nella fase 2 del progetto.
- `pandoc.py`: conterrà il parser per le estensioni specifiche di Pandoc, come le task list, il testo barrato, il testo in apice e pedice, e le note a piè di pagina. Anche questo modulo è attualmente vuoto e sarà implementato nella fase 2.
"""

from .standard import MarkdownParser, ParseInline, MakeParagraph

__all__: list[str] = ["MarkdownParser", "ParseInline", "MakeParagraph"]
