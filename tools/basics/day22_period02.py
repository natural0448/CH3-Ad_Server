"""Keep the existing classroom command and run the lesson's canonical script."""
from pathlib import Path
import runpy


def main():
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "day22_crud.py"), run_name="__main__")


if __name__ == "__main__":
    main()
