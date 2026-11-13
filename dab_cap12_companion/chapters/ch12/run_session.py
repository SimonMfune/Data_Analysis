"""Runs the Chapter 12 listings in order in one shared session (as in a notebook) and saves each output.

Run from the repository root:  python chapters/ch12/run_session.py
"""
import contextlib
import io
from pathlib import Path

HERE = Path(__file__).resolve().parent
namespace = {"__name__": "__main__"}
for path in sorted((HERE / "listings").glob("12_*.py")):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exec(compile(path.read_text(), str(path), "exec"), namespace)
    (HERE / "outputs" / f"{path.stem}.txt").write_text(buffer.getvalue())
    print(f"ran {path.name}")
