# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-02

### Added

- **Markdown Parser (Phase 1 - Vanilla CommonMark)**
  - Complete support for vanilla markdown syntax
  - Block elements: headings, paragraphs, code blocks, blockquotes, lists, tables, images, formulas, HTML blocks
  - Inline elements: bold, italic, links, code, math, images, line breaks, HTML inline
  - Modular architecture with stubs for Pandoc and HTML tag extensions (Phase 2)

- **TXT Parser**
  - Simple plain text to LaTeX conversion
  - Automatic encoding detection with chardet
  - UTF-8 BOM handling

- **LaTeX Generator**
  - Converts AST to production-ready LaTeX code
  - Image auto-numbering (Fig. 1, Fig. 2, ...)
  - Proper caption positioning within images
  - Support for mathematical formulas and syntax-highlighted code blocks
  - LaTeX package support: graphicx, amsmath, float, makecell, ulem, titlesec, xcolor

- **Documentation**
  - Comprehensive README with architecture overview
  - Universal converter concept (supports multiple input formats)
  - Phase-based roadmap (0.1.x for markdown, 0.2+ for new parsers)
  - Test coverage with vanilla markdown test file

- **Project Structure**
  - Setup.py for package distribution
  - MIT License for open-source usage
  - Clear CLI interface: `python main.py <input> <output>`

### Roadmap

**v0.1.1** - Pandoc Markdown Extensions

- Task Lists, Strikethrough, Superscript/Subscript, Footnotes

**v0.1.2** - HTML Tag Extensions

- HTML <sup>, <sub>, <mark> tag support in markdown

**v0.2.0** - HTML Parser

- Full HTML document parsing and conversion to LaTeX

**v0.3.0** - DOCX Parser

- Microsoft Word document support

**v0.4.0** - PDF Parser

- PDF document parsing and conversion

**Future - GUI & Desktop App**

- Graphical interface with file chooser and output configuration
- Standalone executable for Windows/macOS/Linux
- Commercial version for monetization

## Development Status

- ✅ Core converter infrastructure
- ✅ Markdown vanilla parsing (tested)
- ✅ TXT parsing with encoding detection
- ✅ LaTeX generation with auto-numbering
- ⏳ Markdown extensions (Pandoc, HTML tags)
- 📋 Additional parsers (HTML, DOCX, PDF)
