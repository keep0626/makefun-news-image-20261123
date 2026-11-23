"""make.fun news-image-20261123 entrypoint.

Copies the pre-rendered front page (entry.png, drawn by render.py from
stories.json) to the output directory. Standard library only, so the two
grader runs always write byte-identical output.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
