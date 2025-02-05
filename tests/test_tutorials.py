from pathlib import Path
import re
import logging
import pytest


logging.getLogger("acquire").setLevel(logging.CRITICAL)

code_block_re = re.compile(r"( *)```python\n(.*?)```", re.DOTALL)
skip = {
    "setup.md",  # has invalid syntax
    "trigger.md",  # has some non-existant paths
}


def tutorials():
    docs_path = Path(__file__).parent.parent / "docs"

    tuts = []
    if (get_started := docs_path / "get_started.md").exists():
        tuts.append(get_started)
    tuts.extend([fn for fn in docs_path.glob("tutorials/*.md") if fn.name not in skip])
    tuts.sort()

    return tuts


@pytest.mark.parametrize("tutorial", tutorials(), ids=lambda x: x.name)
def test_tutorials(tutorial: Path):
    for code_block in code_block_re.finditer(tutorial.read_text()):
        whitespace = code_block.group(1)
        if whitespace:
            code_block = "\n".join(line[len(whitespace):] for line in code_block.group(2).split("\n"))
        else:
            code_block = code_block.group(2)
        exec(code_block)
