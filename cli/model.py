from typing import *
from dataclasses import dataclass, field
import re

@dataclass(order=True, frozen=True)
class Version(object):
	"""
	Specify version of a package. Exact version only, no wildcards allowed.
	"""
	major: int
	minor: int
	patch: int

	@staticmethod
	def from_str(s: str):
		num_rx = '(0|[1-9]\d*)'
		ver_rx = f'{num_rx}[.]{num_rx}[.]{num_rx}'
		matches =  re.match(ver_rx, s)
		if not matches:
			raise Exception(f'Expected version to be in * or X.Y.Z format but got {s}')
		nums = matches.groups()

		return Version(int(nums[0]), int(nums[1]), int(nums[2]))

	def __repr__(self):
		return self.to_str()

	def to_str(self) -> str:
		return f'{self.major}.{self.minor}.{self.patch}'

@dataclass(frozen=True)
class Dep(object):
	name: str           # name of the dependent package
	version: str        # version requirement of the dependent packages to use. Use microsoft nuget syntax - https://docs.microsoft.com/en-us/nuget/concepts/package-versioning#version-ranges-and-wildcards

	@staticmethod
	def from_dict(d: Dict[str, Any]):
		return Dep(**d)

@dataclass(frozen=True)
class Package(object):
	name: str               # unique name of the package
	description: str        # description of the package
	version: Version        # version of the package
	tags: List[str]                 = field(default_factory=lambda : [])
	dependencies: List[Dep]         = field(default_factory=lambda : [])
	monitors: List[str]             = field(default_factory=lambda : [])
	events: List[str]               = field(default_factory=lambda : [])
	connectivityPlugins: List[str]  = field(default_factory=lambda : [])

	def __post_init__(self):
		if isinstance(self.version, str):
			raise Exception('Pass Version object instead of version string')

	@staticmethod
	def from_dict(dict: Dict[str, Any]):
		if 'dependencies' in dict:
			deps = dict['dependencies']
			for i,d in enumerate(deps):
				if not isinstance(d, Dep):
					deps[i] = Dep.from_dict(d)
			dict['dependencies'] = deps
		if 'version' in dict:
			if isinstance(dict['version'], str):
				dict['version'] = Version.from_str(dict['version'])
		return Package(**dict)