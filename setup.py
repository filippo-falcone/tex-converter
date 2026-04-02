from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description: str = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements: list[str] = [line.strip() for line in fh if line.strip()]

setup(
    name="tex-converter",
    version="0.1.0",
    author="Filippo Falcone",
    author_email="falconefilippo98@hotmail.com",
    description="Universal converter from multiple formats (TXT, Markdown, HTML, DOCX, PDF) to LaTeX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filippo-falcone/tex-converter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    keywords="markdown latex pdf converter text-processing",
    project_urls={
        "Bug Reports": "https://github.com/filippo-falcone/tex-converter/issues",
        "Source": "https://github.com/filippo-falcone/tex-converter",
        "Documentation": "https://github.com/filippo-falcone/tex-converter/blob/main/README.md",
    },
)
