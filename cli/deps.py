# dependencies management of Apama packages

from common.model import *
from dataclasses import dataclass, field
import re, collections



@dataclass
class VersionRequirement(object):
	"""
	Version requirement for a dependency. Allows wildcard
	"""
	major: str
	minor: str
	patch: str

	@staticmethod
	def from_str(s: str):
		if s == '*':
			return VersionRequirement('*', '*', '*')

		num_rx = '(0|\*|[1-9]\d*)'
		ver_rx = f'{num_rx}[.]{num_rx}[.]{num_rx}'
		matches =  re.match(ver_rx, s)
		if not matches:
			raise Exception(f'Expected version requirement to be in * or X.Y.Z format but got {s}')
		nums = matches.groups()

		return VersionRequirement(nums[0], nums[1], nums[2])


# cache of package versions
pkg_versions: Dict[str, List[Version]] = {}

# cache of package information
pkg_info: Dict[str: Dict[Version, Package]] = {}


def get_pkg_versions(name: str) -> List[Version]:
	if name in pkg_versions:
		return pkg_versions[name]

	# TODO: else make HTTP call to the backend and cache the information
	return []

def get_latest_version(name: str) -> Version:
	return sorted(get_pkg_versions(name))[-1]


def get_pkg_info(name: str, version: Optional[str] = None) -> Package:
	if not version:
		version =get_latest_version(name)

	if name in pkg_info:
		if version in pkg_info[name]:
			return pkg_info[name][version]

	# TODO: make HTTP call to the backend and cache the information
	return None


def find_dependencies(name: str, version: Optional[str]) -> Dict[str, Version]:
	"""
	Find all dependencies of the provided package.
	:param name: The package name whose dependencies need to be found.
	:param version: The package version. Use latest if not specified. Currently ignored.
	:return: Dependent package names along with the version to use. Includes the current package as well.
	"""

	# very basic for now - just pick the latest version of the dependencies
	visited = {}
	parent = {}
	queue = collections.deque[name]
	visited[name] = get_latest_version(name)

	while queue:
		pkg_name = queue.popleft()
		pkg_info = get_pkg_info(pkg_name)   # latest for now
		for dep in pkg_info.dependencies:
			if dep.name not in visited:
				visited[dep.name] = get_latest_version(dep.name)
				queue.append(dep.name)
				parent[dep.name] = pkg_name
			else:
				if parent[dep.name] != pkg_name:
					raise Exception('cyclic dependency found')

	return visited

