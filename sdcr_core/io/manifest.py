# sdcr_core/io/manifest.py

"""
Manifest Module for SDCR-CORE v0.2.
Generates an integrity manifest detailing all generated outputs.
"""

import os
import json
import hashlib
from typing import Dict, Any

def compute_sha256(filepath: str) -> str:
    """Computes the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def generate_manifest(output_dir: str = "results") -> None:
    """
    Generates a manifest.json file in the output directory
    listing all files, their sizes, and SHA-256 checksums.
    """
    manifest_data: Dict[str, Dict[str, Any]] = {}

    for filename in sorted(os.listdir(output_dir)):
        if filename == "manifest.json":
            continue
        filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            checksum = compute_sha256(filepath)
            manifest_data[filename] = {
                "size_bytes": file_size,
                "sha256": checksum
            }

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=4)
