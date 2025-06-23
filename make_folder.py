from pathlib import Path

WORK_DIR = Path(__file__).parent
OUT_DIR, IN_DIR = WORK_DIR / "output", WORK_DIR / "input"

if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    IN_DIR.mkdir(exist_ok=True)