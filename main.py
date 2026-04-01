import sys
from src.tex_converter.converter import Convert


def Main() -> None:
    if len(sys.argv) < 3:
        print("Uso corretto: python main.py <input_file> <output_file>")
        return
    InputPath: str = sys.argv[1]
    Outpath: str = sys.argv[2]
    print(f"Converto {InputPath} in {Outpath} ... ")
    Convert(InputPath, Outpath)
    print("Conversione completata!")


if __name__ == "__main__":
    Main()
