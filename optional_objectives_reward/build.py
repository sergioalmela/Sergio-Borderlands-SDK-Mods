#!/usr/bin/env python3
"""Build script to create .sdkmod file for Optional Objectives Reward mod."""

import zipfile
from pathlib import Path

# Configuration
MOD_FOLDER = Path(__file__).parent
MOD_NAME = "optional_objectives_reward"
OUTPUT_FILE = MOD_FOLDER / f"{MOD_NAME}.sdkmod"

# Files to include in the package
FILES_TO_PACKAGE = [
    "__init__.py",
    "pyproject.toml",
    "README.md",
    "LICENSE",
]


def create_sdkmod():
    """Create the .sdkmod package file."""
    print(f"Creating {OUTPUT_FILE.name}...")

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
        for filename in FILES_TO_PACKAGE:
            file_path = MOD_FOLDER / filename

            if not file_path.exists():
                print(f"Warning: {filename} not found, skipping...")
                continue

            # Add to zip with mod folder structure
            archive_path = f"{MOD_NAME}/{filename}"
            zip_file.write(file_path, archive_path)
            print(f"  Added: {filename}")

    print(f"\n✅ Successfully created: {OUTPUT_FILE}")
    print(f"   Size: {OUTPUT_FILE.stat().st_size:,} bytes")


if __name__ == "__main__":
    create_sdkmod()