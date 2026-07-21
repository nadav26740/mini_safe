#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def run(cmd, cwd=None):
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def ensure_build_tools():
    try:
        import build  # noqa: F401
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "build"])


def build_python_artifacts():
    ensure_build_tools()
    DIST.mkdir(exist_ok=True)
    run([sys.executable, "-m", "build"], cwd=ROOT)


def build_debian_package():
    print("Debian build requires dpkg-buildpackage and related tools.")
    print("Run: dpkg-buildpackage -us -uc")


def build_fedora_package():
    print("Fedora build requires rpmbuild and rpmdevtools.")
    print("Run:")
    print("  rpmdev-setuptree")
    print("  cp dist/mini-safe-1.0.0.tar.gz ~/rpmbuild/SOURCES/")
    print("  cp packaging/fedora/mini-safe.spec ~/rpmbuild/SPECS/")
    print("  rpmbuild -ba ~/rpmbuild/SPECS/mini-safe.spec")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
        if target == "python":
            build_python_artifacts()
        elif target == "debian":
            build_debian_package()
        elif target == "fedora":
            build_fedora_package()
        else:
            raise SystemExit("Usage: python scripts/build_packages.py [python|debian|fedora]")
    else:
        build_python_artifacts()
        build_debian_package()
        build_fedora_package()
