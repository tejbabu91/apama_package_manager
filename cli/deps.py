# dependencies management of Apama packages

from common.model import *
from dataclasses import dataclass, field
import re, collections
from enum import Enum


class Boundary(Enum):
	INCLUSIVE = 1
	EXCLUSIVE = 2

@dataclass(order=False)
class VersionRange(object):
	"""
	Version requirement for a dependency.
	"""

	start: Optional[Tuple[int, int, Boundary]]
	end: Optional[Tuple[int, int, Boundary]]

	@staticmethod
	def from_str(orig_str: str):
		s = orig_str.strip()
		def parse_num(n: str) -> Tuple[int, int]:
			n = n.strip()
			matches = re.match('(\d+)\.(\d+)(.\d+)?', n)
			if not matches:
				raise Exception(f'Invalid version string: {n}')
			nums = matches.groups()
			if len(nums) >= 3 and nums[2] is not None:
				print(f'Ignoring patch version part while parsing version number: {n}')
			return int(nums[0]), int(nums[1])

		start = None
		end = None
		start_boundary = None
		end_boundary = None
		if s.startswith('['):
			start_boundary = Boundary.INCLUSIVE
			s = s[1:]
		elif s.startswith('('):
			start_boundary = Boundary.EXCLUSIVE
			s = s[1:]

		if s.endswith(']'):
			end_boundary = Boundary.INCLUSIVE
			s = s[:-1]
		elif s.endswith(')'):
			end_boundary = Boundary.EXCLUSIVE
			s = s[:-1]
		if start_boundary or end_boundary:
			# either both are provide or none is provided
			if not (start_boundary and end_boundary):
				raise Exception(f'Only one of the start and end boundary specified; either specify both or none: {orig_str}')
		ranges = s.split(',')

		# basic checking
		if len(ranges) == 1:
			num = ranges[0].strip()
			if num == '': raise Exception(f'Invalid version requirement: {orig_str}')
		elif len(ranges) > 2:
			raise Exception(f'Invalid range specified; expected start and end only: {orig_str}')

		if start_boundary is None and end_boundary is None:
			if len(ranges) == 1:
				nums = parse_num(ranges[0])
				# range is >= num
				start = (nums[0], nums[1], Boundary.INCLUSIVE)
				end = None
			else:
				raise Exception(f'Invalid range specified: {orig_str}; Use [, ], ( and ) to in close range.')
		else:
			# both boundary specified
			if len(ranges) == 1:
				if start_boundary == Boundary.INCLUSIVE and end_boundary == Boundary.INCLUSIVE:
					nums = parse_num(ranges[0])
					start = (nums[0], nums[1], Boundary.INCLUSIVE)
					end = start
				else:
					raise Exception(f'Only [major.minor] format is allowed without specifying start and end: {orig_str}')
			if len(ranges) == 2:
				start_str = ranges[0].strip()
				end_str = ranges[1].strip()
				if start_str == '' and end_str == '':
					raise Exception(f'Both start and end range cannot be empty, specify at least one: {orig_str}')
				if start_str:
					nums = parse_num(start_str)
					start = (nums[0], nums[1], start_boundary)
				else:
					start = None

				if end_str:
					nums = parse_num(end_str)
					end = (nums[0], nums[1], end_boundary)
				else:
					end = None


		return VersionRange(start=start, end=end)


	def __repr__(self):
		res = ''
		if self.start:
			if self.start[2] == Boundary.INCLUSIVE:
				res = '['
			else:
				res = '('

			res = f'{res}{self.start[0]}.{self.start[1]},'
		else:
			res = '(,'

		if self.end:
			res = f'{res}{self.end[0]}.{self.end[1]}'

			if self.end[2] == Boundary.INCLUSIVE:
				res = f'{res}]'
			else:
				res = f'{res})'
		else:
			res = f'{res})'

		return res



# cache of package versions
pkg_versions: Dict[str, List[Version]] = {}

# cache of package information
pkg_info: Dict[str, Dict[Version, Package]] = {}


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
	queue = collections.deque[name]
	visited[name] = get_latest_version(name)

	while queue:
		pkg_name = queue.popleft()
		pkg_info = get_pkg_info(pkg_name)   # latest for now
		for dep in pkg_info.dependencies:
			if dep.name not in visited:
				visited[dep.name] = get_latest_version(dep.name)
				queue.append(dep.name)



	return visited



def test_version_range_parsing():
	for s in [
		'1.0',

		'[1.0]',

		'[1.0,]',
		'[1.0,)',
		'[,1.0]',
		'[,1.0)',

		'(1.0,)',
		'(1.0,]',
		'(,1.0)',
		'(,1.0]',

		'[1.0,2.0]',
		'(1.0,2.0)',
		'(1.0,2.0]',
		'[1.0,2.0)',

		# invalid
		'(1.0)',
		'(1.0',
		'[1.0)',
		'[1.0,2.3,4.5]',
	]:
		result = ''
		try:
			v = VersionRange.from_str(s)
			result = str(v)
		except Exception as ex:
			result = str(ex)
		print(f'{s}:    {result}')

if __name__ == '__main__':
	test_version_range_parsing()