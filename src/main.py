from string import ascii_uppercase

from rich.console import Console
from typer import Typer

from src.alphabet import Alphabet

app = Typer()
console = Console()


@app.command()
def eng_alphabet() -> None:
    console.print(Alphabet('English', ascii_uppercase, 13), justify='center')


if __name__ == "__main__":
    app()
