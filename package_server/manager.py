import os
from json import load

class Manager:
    def __init__(self, package_dir):
        self.manifest_path = os.path.join(package_dir, 'manifest.json')
        with open(self.manifest_path, 'r') as f:
            self.manifest_data = load(f)
