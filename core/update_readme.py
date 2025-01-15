import os
import re

def get_version():
    """
    Reads core/version.py and extracts the __version__ string.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    version_file = os.path.join(base_dir, "core", "version.py")
    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string in core/version.py")

def update_readme(readme_path, version):
    """
    Replaces the {{VERSION}} placeholder in the README with the version.
    """
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace("{{VERSION}}", version)
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {readme_path} to version {version}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_file = os.path.join(base_dir, "README.md")
    version = get_version()
    update_readme(readme_file, version)