import re
import shutil
from pathlib import Path


def search(pattern: str, root: str = "."):
    root_path = Path(root)
    regex = re.compile(pattern)
    results: list[tuple[Path, int, str]] = []

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        try:
            for lineno, line in enumerate(path.open(encoding="utf-8", errors="ignore"), 1):
                if regex.search(line):
                    results.append((path, lineno, line.rstrip()))
        except (UnicodeDecodeError, PermissionError):
            continue

    if not results:
        print("Ничего не найдено.")
        return

    width = shutil.get_terminal_size().columns
    print(f"Найдено {len(results)} совпадений:\n")
    for i, (path, lineno, text) in enumerate(results, 1):
        print(f"[{i}] {path}:{lineno}\n    {text[:width - 8]}")
    print()

    try:
        choice = int(input("Выбери номер для открытия (0 — выход): "))
    except ValueError:
        return
    if not 1 <= choice <= len(results):
        return

    file, line, _ = results[choice - 1]
    open_at_line(file, line)


def open_at_line(file: Path, line: int) -> None:
    if shutil.which("pycharm"):
        import subprocess
        subprocess.run(["pycharm", "--line", str(line), str(file)])
    elif shutil.which("vim"):
        import subprocess
        subprocess.run(["vim", f"+{line}", str(file)])
    else:
        print(f"{file}:{line}")


if __name__ == '__main__':
    search('class', 'src')