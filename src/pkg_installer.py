import sys
import subprocess

try:  # On import error install setuptools package
    import pkg_resources  # type: ignore
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "setuptools"])

import pkg_resources  # type: ignore


def pkg_installer() -> None:
    """
        Automatic package installation
    """
    filename = "./requirements.txt"
    lines = None
    try:
        # read lines from requirement.txt
        with open(filename, 'r') as file:  # read lines from requirement.txt
            lines = file.readlines()

        lines = [x.strip() for x in lines]  # clean list data

        if not lines:  # package list is empty
            print("Info: No packages")
            return

        for package_name in lines:
            try:
                # check if each package is already installed
                pkg_resources.get_distribution(package_name)
                print(f"{package_name} is already installed")

            except pkg_resources.DistributionNotFound as e:
                print(f"{package_name} not installed\nInstalling......")
                try:
                    # install
                    subprocess.check_call(
                        [sys.executable, '-m', 'pip', 'install', package_name])
                except Exception as e:
                    print(f"Error: {str(e)}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    pkg_installer()
