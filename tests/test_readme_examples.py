"""Run the README's Python examples and compare their output to the README.

Each ```python block that is directly followed by a ```bash block (optionally
inside a collapsible <details><summary>...</summary> section) is executed, and
what it prints must match the bash block exactly, so the README cannot drift
from the library's actual behaviour.
"""

import contextlib
import io
import re
from pathlib import Path

import pytest

README = Path(__file__).resolve().parent.parent / "README.md"
EXAMPLE_RE = re.compile(
    r"```python\n((?:(?!```).)*)```\n"
    r"(?:\s*<details>\s*<summary>[^<]*</summary>\s*)?"
    r"```bash\n(.*?)```",
    re.DOTALL,
)
EXAMPLES = EXAMPLE_RE.findall(README.read_text(encoding="utf-8"))


def test_readme_has_examples():
    assert len(EXAMPLES) >= 2


@pytest.mark.parametrize(
    "code, expected", EXAMPLES, ids=[f"example{i}" for i in range(len(EXAMPLES))]
)
def test_readme_example(code: str, expected: str) -> None:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(compile(code, str(README), "exec"), {})
    assert stdout.getvalue().rstrip() == expected.rstrip()
