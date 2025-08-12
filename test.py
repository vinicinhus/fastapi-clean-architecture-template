from pathlib import Path
from typing import Union, Iterable

def print_tree(path: Union[str, Path], prefix: str = "", ignore: Iterable[str] = ("__pycache__", ".venv")) -> None:
    """
    Mostra a árvore de diretórios e arquivos ignorando diretórios especificados.

    Args:
        path (str | Path): Caminho inicial da árvore.
        prefix (str): Prefixo usado na indentação (usado internamente na recursão).
        ignore (Iterable[str]): Lista de nomes de diretórios/arquivos a serem ignorados.
    """
    path = Path(path)
    contents = [p for p in sorted(path.iterdir()) if p.name not in ignore]
    pointers = ['├── '] * (len(contents) - 1) + ['└── ']

    for pointer, p in zip(pointers, contents):
        print(prefix + pointer + p.name)
        if p.is_dir():
            print_tree(p, prefix + ('│ ' if pointer == '├── ' else '    '), ignore)

# Exemplo de uso:
print_tree(".", ignore=("__pycache__", ".venv", ".git", "node_modules"))