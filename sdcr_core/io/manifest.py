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

def generate_manifest(
    results_dir: str = "results",
    figures_dir: str = "figures",
    zip_filepath: str = "SDCR_CORE_V02_RESULT_PACKAGE.zip"
) -> None:
    """
    Generates a results/SHA256_MANIFEST.json file
    listing all files, their sizes, and SHA-256 checksums,
    including the final ZIP package.
    """
    manifest_data: Dict[str, Dict[str, Any]] = {}

    # Helper to add files from a directory
    def add_dir_files(directory: str, prefix: str):
        if not os.path.exists(directory):
            return
        for filename in sorted(os.listdir(directory)):
            if filename == "SHA256_MANIFEST.json":
                continue
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                file_size = os.path.getsize(filepath)
                checksum = compute_sha256(filepath)
                # Store under prefix/filename (or just filename if no prefix)
                key = os.path.join(prefix, filename) if prefix else filename
                manifest_data[key] = {
                    "size_bytes": file_size,
                    "sha256": checksum
                }

    # Add results files (flat)
    add_dir_files(results_dir, prefix="")
    # Add figures files (under figures/ prefix)
    add_dir_files(figures_dir, prefix="figures")

    # Add the final ZIP package
    if os.path.exists(zip_filepath):
        file_size = os.path.getsize(zip_filepath)
        checksum = compute_sha256(zip_filepath)
        manifest_data[os.path.basename(zip_filepath)] = {
            "size_bytes": file_size,
            "sha256": checksum
        }

    manifest_path = os.path.join(results_dir, "SHA256_MANIFEST.json")
    os.makedirs(results_dir, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=4)
