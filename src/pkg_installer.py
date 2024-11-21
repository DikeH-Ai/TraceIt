import sys
import subprocess
import importlib.metadata
from typing import List


def pkg_installer() -> None:
    """Automatic Package installer"""
    filename = "./requirements.txt"
    lines = None

    try:
        # Read lines from requirements.txt
        with open(filename, 'r') as file:
            lines = file.readlines()

        lines = [x.strip() for x in lines]  # Clean list data

        if not lines:  # Package list is empty
            print("Info: No packages")
            return

        for package_name in lines:
            try:
                # Check if each package is already installed
                importlib.metadata.version(package_name)
                print(f"{package_name} is already installed")
            except importlib.metadata.PackageNotFoundError:
                print(f"{package_name} not installed\nInstalling......")
                try:
                    # Install package
                    subprocess.check_call(
                        [sys.executable, '-m', 'pip', 'install', package_name])
                except subprocess.CalledProcessError as e:
                    print(f"Error during installation of {
                          package_name}: {str(e)}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    pkg_installer()
