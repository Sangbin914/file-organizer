from pathlib import Path
import json
import shutil
from datetime import datetime

DEFAULT_RULES = {
    "pdf": "PDFs",
    "png": "Images",
    "jpg": "Images",
    "jpeg": "Images",
    "gif": "Images",
    "zip": "Archives",
    "rar": "Archives",
    "7z": "Archives",
    "txt": "Text",
    "csv": "Data",
    "py": "Code",
    "cpp": "Code",
    "h": "Code",
}

def load_rules(rules_path: Path) -> dict:
    if rules_path.exists():
        return json.loads(rules_path.read_text())
    return DEFAULT_RULES

def unique_path(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while True:
        candidate = dest.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1

def organize(folder: Path, rules: dict, dry_run: bool = True):
    moves = []
    for p in folder.iterdir():
        if p.is_dir():
            continue
        ext = p.suffix.lower().lstrip(".")
        target_dirname = rules.get(ext, "Other")
        target_dir = folder / target_dirname
        target_path = unique_path(target_dir / p.name)
        moves.append((p, target_path))

    # Preview
    print(f"Found {len(moves)} files to organize (dry_run={dry_run})")
    for src, dst in moves[:30]:
        print(f"{src.name}  ->  {dst.parent.name}/{dst.name}")
    if len(moves) > 30:
        print(f"... and {len(moves) - 30} more")

    if dry_run:
        return

    # Execute
    log_lines = []
    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        log_lines.append(f"{datetime.now().isoformat()} MOVED {src} -> {dst}")

    log_dir = folder / "logs"
    log_dir.mkdir(exist_ok=True)
    (log_dir / "organizer.log").write_text("\n".join(log_lines))

if __name__ == "__main__":
    folder = Path.home() / "Downloads"   # 필요하면 바꾸기
    rules = load_rules(Path("rules.json"))
    organize(folder, rules, dry_run=True)  # 처음엔 True 추천

