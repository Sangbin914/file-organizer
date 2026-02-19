from pathlib import Path
import json
import shutil
from datetime import datetime
import argparse


def load_rules(rules_path: Path) -> dict:
    if rules_path.exists():
        return json.loads(rules_path.read_text(encoding="utf-8"))
    return {}


def unique_path(dest: Path) -> Path:
    """If dest exists, append _1, _2, ... before suffix."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    i = 1
    while True:
        candidate = dest.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def plan_moves(folder: Path, rules: dict) -> list[tuple[Path, Path]]:
    moves = []
    for p in folder.iterdir():
        if p.is_dir():
            continue
        ext = p.suffix.lower().lstrip(".")
        target_dirname = rules.get(ext, "Other")
        target_dir = folder / target_dirname
        target_path = unique_path(target_dir / p.name)
        moves.append((p, target_path))
    return moves


def write_log(log_path: Path, lines: list[str]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(lines), encoding="utf-8")


def organize(folder: Path, rules_path: Path, dry_run: bool) -> None:
    if not folder.exists():
        raise FileNotFoundError(f"Target folder does not exist: {folder}")

    rules = load_rules(rules_path)
    moves = plan_moves(folder, rules)

    print(f"Target: {folder}")
    print(f"Planned moves: {len(moves)} (dry_run={dry_run})")

    # Preview first 30
    for src, dst in moves[:30]:
        print(f"- {src.name}  ->  {dst.parent.name}/{dst.name}")
    if len(moves) > 30:
        print(f"... and {len(moves) - 30} more")

    if dry_run:
        print("Dry-run complete. No files were moved.")
        return

    log_lines = []
    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        log_lines.append(f"{datetime.now().isoformat()} MOVED {src.name} -> {dst.parent.name}/{dst.name}")

    log_path = folder / "logs" / "organizer.log"
    write_log(log_path, log_lines)
    print(f"Done. Log written to: {log_path}")


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by extension.")
    parser.add_argument("--folder", type=str, default=str(Path.home() / "Desktop" / "organizer_test"),
                        help="Target folder to organize (default: ~/Desktop/organizer_test)")
    parser.add_argument("--rules", type=str, default="rules.json",
                        help="Path to rules.json (default: rules.json)")
    parser.add_argument("--execute", action="store_true",
                        help="Actually move files (otherwise dry-run)")
    args = parser.parse_args()

    organize(Path(args.folder), Path(args.rules), dry_run=not args.execute)


if __name__ == "__main__":
    main()
