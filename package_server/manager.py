import os
from dataclasses_json import dataclass_json
from dataclasses import dataclass, field
from typing import *
import zipfile
import shutil
import model


@dataclass_json
@dataclass(order=True)
class Manifest:
    """
    Class representing metadata of repository
    """
    packages: List[model.Package] = field(default_factory=lambda: [])

class Manager:
    MANIFEST_NAME = 'apama_packages.json'
    def __init__(self, package_dir):
        self.manifest_path = os.path.join(package_dir, self.MANIFEST_NAME)
        self.data_path = os.path.join(package_dir, 'data')
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)
        if os.path.isfile(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                self.manifest_data = Manifest.from_json('\n'.join(f.readlines()))
                print(self.manifest_data)
        else:
            self.manifest_data = Manifest()
            with open(self.manifest_path, 'w') as f:
                f.write(self.manifest_data.to_json())

    def create_dirs(self):
        os.makedirs(os.path.dirname(self.manifest_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)

    def write_manifest(self):
        with open(self.manifest_path, 'w') as f:
            f.write(self.manifest_data.to_json())

    def get_package_path(self, manifest):
        """
        Return the path to package stored on disk.

        :param manifest:
        :return:
        """
        return os.path.join(self.data_path, f'{manifest.name}', f'{manifest.version}', 'package.zip')

    def get_package_manifest(self, name, version):
        """
        Return the package manifest matching the name and version.

        :param name:
        :param version:
        :return:
        """
        for p in self.manifest_data.packages:
            if p.name == name and p.version == version:
                return p
        return None

    def get_manifest_json(self):
        """
        Return the full manifest as JSON

        :return:
        """
        return self.manifest_data.to_json()

    def get_package_manifests_by_name(self, name):
        """
        Return a package manifest and path.

        :param name:
        :return:
        """
        return [x for x in self.manifest_data.packages if x.name == name]

    def add_package(self, data_file_path):
        with zipfile.ZipFile(data_file_path, 'r') as z:
            m = z.extract(self.MANIFEST_NAME)
            with open(m, 'r') as f:
                data = f.read()
            manifest = model.Package.from_json(data)

        for (i, p) in enumerate(self.manifest_data.packages):
            if p.name == manifest.name and p.version == manifest.version:
                del self.manifest_data.packages[i]

        self.manifest_data.packages.append(manifest)
        self.write_manifest()

        package_dir = os.path.join(self.data_path, f'{manifest.name}', f'{manifest.version}')
        os.makedirs(package_dir, exist_ok=True)
        if os.path.exists(os.path.join(package_dir, 'package.zip')): os.remove(os.path.join(package_dir, 'package.zip'))
        shutil.move(data_file_path, os.path.join(package_dir, 'package.zip'))









