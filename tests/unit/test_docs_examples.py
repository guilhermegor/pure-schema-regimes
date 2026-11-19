"""Run every ``python`` code block in the README and usage docs, so no example rots."""

from pathlib import Path
import re

import pytest


_PATH_ROOT = Path(__file__).parents[2]
_RE_PYTHON_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)


def _read_python_blocks(path_doc: Path) -> str:
    """Join a document's ``python`` code blocks, in order, into one script.

    Parameters
    ----------
    path_doc : pathlib.Path
        The Markdown document.

    Returns
    -------
    str
        The blocks joined by newlines; later blocks reuse names earlier ones define.
    """
    return "\n".join(_RE_PYTHON_BLOCK.findall(path_doc.read_text(encoding="utf-8")))


@pytest.mark.parametrize(
    "str_doc", ["README.md", "docs/usage.md", "docs/examples.md"], ids=lambda str_doc: str_doc
)
def test_docs_examples_python_blocks_run(str_doc: str) -> None:
    """Every documented example runs top to bottom and builds the shared registry.

    Parameters
    ----------
    str_doc : str
        Path of the document, relative to the project root.

    Returns
    -------
    None
    """
    path_doc = _PATH_ROOT / str_doc
    obj_code = compile(_read_python_blocks(path_doc), str(path_doc), "exec")
    dict_namespace: dict[str, object] = {}
    exec(obj_code, dict_namespace)  # noqa: S102 - runs this repo's own docs, nothing external
    assert "cls_registry" in dict_namespace
