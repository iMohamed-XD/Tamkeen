from pathlib import Path
import uuid

DATA_DIR = Path("C:\\Tamkeen\\9-DL_project\\data")          # path to your data folder
SEPARATOR = "_"                  # "pencil_1"; use " " for "pencil 1"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".heif", ".tiff", ".tif"}  # file extensions to rename
DRY_RUN = False                   # set to False to actually rename

for folder in sorted(p for p in DATA_DIR.iterdir() if p.is_dir()):
    # Deterministic order: sorted by current filename
    files = sorted(f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in EXTS)
    width = len(str(len(files)))  # number of digits in the total count

    # Pass 1: move to unique temp names (avoids collisions)
    temps = []
    for f in files:
        tmp = f.with_name(f"__tmp_{uuid.uuid4().hex}{f.suffix}")
        if not DRY_RUN:
            f.rename(tmp)
        temps.append((f, tmp))

    # Pass 2: temp names to final names
    for i, (orig, tmp) in enumerate(temps, start=1):
        final = folder / f"{folder.name}{SEPARATOR}{i:0{width}d}{orig.suffix.lower()}"
        print(f"{orig.name} -> {final.name}")
        if not DRY_RUN:
            tmp.rename(final)