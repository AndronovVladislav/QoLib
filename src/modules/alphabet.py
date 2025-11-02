from rich import box
from rich.table import Table


class Alphabet:

    def __init__(self, name: str, alphabet: str, line_len: int):
        self._name = name
        self._alphabet = alphabet
        self._line_len = line_len

    def __rich__(self) -> Table:
        table = Table(
            title=f'{self._name.capitalize()} alphabet',
            header_style=None,
            box=box.ROUNDED,
            show_lines=True,
        )

        for letter in self._alphabet[:self._line_len]:
            table.add_column(letter)

        for i in range(self._line_len, len(self._alphabet), self._line_len):
            table.add_row(*self._alphabet[i:i + self._line_len])

        return table
