#!/usr/bin/env python3
"""
SDCR-CORE Launcher
==================

Single-entry launcher for the SDCR read-only visualization.

This script exists purely for convenience:
- No parameters
- No configuration
- No logic beyond delegation

It launches the hardened interferometry visualization
with full validation enabled.

Usage:
    python scripts/run_visualizer.py
    
    or (if executable):
    ./scripts/run_visualizer.py
"""

from __future__ import annotations

import sys
import os
from pathlib import Path


def _validate_environment() -> Path:
    """
    Validate execution environment and return repository root.
    
    Returns:
        Path: Absolute path to repository root
        
    Raises:
        RuntimeError: If environment is invalid
    """
    # Determine script location
    script_path = Path(__file__).resolve()
    
    # Expected structure: sdcr-core/scripts/run_visualizer.py
    repo_root = script_path.parent.parent
    
    # Verify we're in the correct repository structure
    expected_dirs = ["core", "examples", "scripts"]
    missing_dirs = [d for d in expected_dirs if not (repo_root / d).is_dir()]
    
    if missing_dirs:
        raise RuntimeError(
            f"Invalid repository structure. Missing directories: {missing_dirs}\n"
            f"Expected to find: {expected_dirs}\n"
            f"Current location: {repo_root}\n"
            "Please run this script from a properly cloned sdcr-core repository."
        )
    
    # Check for critical files
    visualizer_path = repo_root / "examples" / "visualize_sdcr.py"
    if not visualizer_path.exists():
        raise RuntimeError(
            f"Visualizer not found at: {visualizer_path}\n"
            "Please ensure examples/visualize_sdcr.py exists."
        )
    
    return repo_root


def _check_dependencies() -> list[str]:
    """
    Check for required Python packages.
    
    Returns:
        List of missing packages (empty if all present)
    """
    required_packages = {
        "numpy": "numpy",
        "matplotlib": "matplotlib",
        "scipy": "scipy",
    }
    
    missing = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    return missing


def main() -> None:
    """Main launcher entry point."""
    print("=" * 70)
    print("SDCR-CORE Visualization Launcher")
    print("=" * 70)
    print()
    
    # Step 1: Validate environment
    try:
        print("⏳ Validating environment...")
        repo_root = _validate_environment()
        print(f"✓ Repository root: {repo_root}")
    except RuntimeError as e:
        print(f"❌ Environment validation failed:\n{e}")
        sys.exit(1)
    
    # Step 2: Add repo to path
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
        print(f"✓ Added to Python path: {repo_root_str}")
    
    # Step 3: Check dependencies
    print("\n⏳ Checking dependencies...")
    missing = _check_dependencies()
    
    if missing:
        print(f"❌ Missing required packages: {', '.join(missing)}")
        print("\nInstall them with:")
        print(f"    pip install {' '.join(missing)}")
        sys.exit(1)
    
    print("✓ All dependencies satisfied")
    
    # Step 4: Import and launch visualizer
    print("\n⏳ Loading visualizer module...")
    try:
        from examples.visualize_sdcr import main as visualize_main
        print("✓ Visualizer loaded successfully")
    except ImportError as e:
        print(f"❌ Failed to import visualizer module:")
        print(f"    {e}")
        print("\nThis usually means:")
        print("  1. The repository structure is incomplete")
        print("  2. Core modules have import errors")
        print("  3. Python version incompatibility (requires Python 3.8+)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error during import:")
        print(f"    {e}")
        sys.exit(1)
    
    # Step 5: Launch
    print("\n" + "=" * 70)
    print("Launching SDCR visualization...")
    print("=" * 70)
    print()
    
    try:
        visualize_main()
    except KeyboardInterrupt:
        print("\n\n⚠ Visualization interrupted by user (Ctrl+C)")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"\n❌ Visualization failed with error:")
        print(f"    {type(e).__name__}: {e}")
        print("\nIf this persists, please check:")
        print("  - Repository integrity")
        print("  - Python environment (virtual environment activated?)")
        print("  - File permissions")
        sys.exit(1)


if __name__ == "__main__":
    # Python version check (bare minimum)
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    main()
