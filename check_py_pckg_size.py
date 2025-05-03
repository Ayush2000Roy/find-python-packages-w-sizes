import json
import subprocess
import os
from importlib import import_module
from tqdm import tqdm
from datetime import datetime

def get_package_size(package_name):
    try:
        module = import_module(package_name)
        package_path = os.path.dirname(module.__file__)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(package_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    except Exception as e:
        return f"Error: {str(e)}"

def get_pip_packages():
    result = subprocess.run(['pip', 'list', '--format=json'], capture_output=True, text=True)
    return json.loads(result.stdout)

def main():
    packages = get_pip_packages()
    package_sizes = {}

    for package in tqdm(packages, desc="Processing packages", unit="package"):
        name = package['name']
        size = get_package_size(name.lower())
        package_sizes[name] = {
            'version': package['version'],
            'size': size if isinstance(size, int) else "Unable to determine size",
            'size_mb': round(size / (1024 * 1024), 2) if isinstance(size, int) else "N/A"
        }

    # Generate a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pip_package_sizes_{timestamp}.json"

    # Save the data to a JSON file
    with open(filename, 'w') as f:
        json.dump(package_sizes, f, indent=2)

    print(f"Package sizes have been saved to {filename}")

if __name__ == "__main__":
    main()