# dependencies management of Apama packages

from model import *
from dataclasses import dataclass
import re, collections
from enum import Enum
import helper

class BoundaryType(Enum):
	INCLUSIVE = 1
	EXCLUSIVE = 2

@dataclass(frozen=True, order=True)
class Boundary(object):
	major: int
	minor: int
	type: BoundaryType

	def is_inclusive(self):
		return self.type == BoundaryType.INCLUSIVE

	def is_exclusive(self):
		return not self.is_inclusive()


@dataclass(order=False, frozen=True)
class VersionRange(object):
	"""
	Version requirement for a dependency.
	"""
	start: Optional[Boundary]   # None means no start
	end: Optional[Boundary]     # None means no end

	@staticmethod
	def from_str(orig_str: Optional[str]):
		if orig_str is None or orig_str == '':
			return VersionRange(start=Boundary(0,0, BoundaryType.INCLUSIVE), end=None)

		s = orig_str.strip()
		def parse_num(n: str) -> Tuple[int, int]:
			n = n.strip()
			matches = re.match('(\d+)\.(\d+)(.\d+)?', n)
			if not matches:
				raise Exception(f'Invalid version string: {n}')
			nums = matches.groups()
			return int(nums[0]), int(nums[1])

		start = None
		end = None
		start_boundary = None
		end_boundary = None
		if s.startswith('['):
			start_boundary = BoundaryType.INCLUSIVE
			s = s[1:]
		elif s.startswith('('):
			start_boundary = BoundaryType.EXCLUSIVE
			s = s[1:]

		if s.endswith(']'):
			end_boundary = BoundaryType.INCLUSIVE
			s = s[:-1]
		elif s.endswith(')'):
			end_boundary = BoundaryType.EXCLUSIVE
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
				start = Boundary(nums[0], nums[1], BoundaryType.INCLUSIVE)
				end = None
			else:
				raise Exception(f'Invalid range specified: {orig_str}; Use [, ], ( and ) to in close range.')
		else:
			# both boundary specified
			if len(ranges) == 1:
				if start_boundary == BoundaryType.INCLUSIVE and end_boundary == BoundaryType.INCLUSIVE:
					nums = parse_num(ranges[0])
					start = Boundary(nums[0], nums[1], BoundaryType.INCLUSIVE)
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
					start = Boundary(nums[0], nums[1], start_boundary)
				else:
					start = None

				if end_str:
					nums = parse_num(end_str)
					end = Boundary(nums[0], nums[1], end_boundary)
				else:
					end = None


		return VersionRange(start=start, end=end)


	def isInRange(self, version: Version) -> bool:
		"""
		Check if a concrete version is in range of the specified version range.
		:param version: The concrete version
		:return: True is specified version satisfies the version range otherwise False.
		"""

		if self.start:
			# the version should be greater than or equal to depending on the boundary
			if self.start.is_inclusive():
				if version.major < self.start.major: return False
				elif version.major == self.start.major:
					if version.minor < self.start.minor: return False
			else:
				if version.major < self.start.major: return False
				elif version.major == self.start.major:
					if version.minor <= self.start.minor: return False

		if self.end:
			if self.end.is_inclusive():
				if version.major > self.end.major: return False
				elif version.major == self.end.major:
					if version.minor > self.end.minor: return False
			else:
				if version.major > self.end.major: return False
				elif version.major == self.end.major:
					if version.minor >= self.end.minor: return False

		return True


	def __repr__(self):
		if self.start:
			res = f'{"[" if self.start.is_inclusive() else "("}{self.start.major}.{self.start.minor}'
		else:
			res = '('
		res = res + ','
		if self.end:
			res = f'{res}{self.end.major}.{self.end.minor}{"]" if self.end.is_inclusive() else ")"}'
		else:
			res = f'{res})'
		return res

	def __post_init__(self):
		if self.start and self.end:
			# make sure end >= start
			if (self.start > self.end) or \
					(self.start.major == self.end.major and self.start.minor == self.end.minor and
					    (self.start.is_exclusive() or self.end.is_exclusive())):
				raise Exception(f'Invalid range {str(self)}, it will never be satisfied')


def find_dependencies_latest_version(name: str) -> Dict[str, Version]:
	"""
	Find all dependencies of the provided package - just return the latest version of all dependencies
	:param name: The package name whose dependencies need to be found.
	:return: Dependent package names along with the version to use. Includes the current package as well.
	"""
	visited = {}
	queue = collections.deque[name]
	visited[name] = helper.get_latest_package(name).version

	while queue:
		pkg_name = queue.popleft()
		pkg_info = helper.get_pkg_info(pkg_name)   # latest for now
		for dep in pkg_info.dependencies:
			if dep.name not in visited:
				visited[dep.name] = helper.get_latest_package(dep.name).version
				queue.append(dep.name)
	return visited

@dataclass(frozen=True)
class PackageRequirement(object):
	name: str                   # name of the package
	version_req: VersionRange   # version requirement

class Conflict(Exception):
	pass

def find_dependencies(packages: List[Tuple[str, Optional[str]]]) -> Dict[str, Version]:
	"""
	Return all dependency packages from list of top level dependency requirements.
	:param packages: List of (package name, version range)
	:return: Dictionary of the all package name and the their version satisfying all package dependency requirements.
	"""
	# TODO: No cycle detection yet.
	def rec_step(selected_versions: Dict[str, Version], open_requirements: Set[PackageRequirement]):
		if not  open_requirements:  # if no more requirements then we are done
			return selected_versions

		## Pick one of the requirement for processing but don't update existing map for easier back tracking
		l = sorted(list(open_requirements), key=lambda x: x.name)


		current_requirement = l[0]
		open_requirements = set(l[1:])  # create copy
		pkg_name = current_requirement.name

		# get selected version if already selected previously else get all available versions and try each
		available_versions =  [selected_versions[pkg_name]] if pkg_name in selected_versions else helper.get_all_package_versions(pkg_name)

		# filter only compatible versions
		compatible_versions = sorted([v for v in available_versions if current_requirement.version_req.isInRange(v)])
		compatible_versions.reverse()
		for ver in compatible_versions:
			try:
				child_selected = selected_versions.copy()
				child_open = open_requirements.copy()

				pkg_info = helper.get_pkg_info(pkg_name, ver)
				child_selected[pkg_name] = ver

				# add all dependencies of the selected package as open requirements
				for dep in pkg_info.dependencies:
					child_open.add(PackageRequirement(dep.name, VersionRange.from_str(dep.version)))
				return rec_step(child_selected, child_open)
			except Conflict as ex:
				pass    # try next version

		raise Conflict(f'No compatible version for requirement {current_requirement}')


	open_requirements: Set[PackageRequirement] = set()
	for (name, version) in packages:
		v = VersionRange.from_str(version)     # any version is ok if none specified
		open_requirements.add(PackageRequirement(name, v))

	return rec_step({}, open_requirements)
