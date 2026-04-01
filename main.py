from src.tex_converter.converter import Convert


def Main() -> None:
    InputPath: str = "sample.txt"
    Outpath: str = "output.tex"
    print(f"Converto {InputPath} in {Outpath} ... ")
    Convert(InputPath, Outpath)
    print("Conversione completata!")


if __name__ == "__main__":
    Main()
