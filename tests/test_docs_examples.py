"""Run every ``.. code-block:: python`` example in the user documentation."""

import contextlib
import io
import re
import textwrap
from pathlib import Path

import pytest

DOCS = Path(__file__).resolve().parent.parent / "docs" / "user"
BLOCK_RE = re.compile(
    r"^\.\. code-block:: python\n\n((?:(?:    .*)?\n)+)", re.MULTILINE
)
EXAMPLES = [
    (f"{page.stem}-{index}", textwrap.dedent(block))
    for page in sorted(DOCS.glob("*.rst"))
    for index, block in enumerate(BLOCK_RE.findall(page.read_text(encoding="utf-8")))
]


def test_docs_have_examples():
    assert len(EXAMPLES) >= 5


@pytest.mark.parametrize("code", [c for _, c in EXAMPLES], ids=[i for i, _ in EXAMPLES])
def test_docs_example_runs(
    code: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)  # examples may write files
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, "docs example", "exec"), {})
