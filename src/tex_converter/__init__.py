"""
tex-converter: Convertitore universale da multiple formati a LaTeX.

Supporta conversione da: TXT, Markdown, HTML, DOCX, PDF → LaTeX.
"""

__version__ = "0.1.0"
__author__ = "Filippo Falcone"
__email__ = "falconefilippo98@hotmail.com"
__license__ = "MIT"

from .converter import Convert

__all__: list[str] = ["Convert"]
