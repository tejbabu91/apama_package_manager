import unittest
from deps import VersionRange
from model import *
import helper, deps

class TestDependencyResolution(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls._original_cache = helper.packages_info_cache.copy()
		helper.packages_info_cache.clear()
		packages = [
			{'name': 'Leaf1', 'description': '', 'version': '1.0.0'},
			{'name': 'Leaf1', 'description': '', 'version': '1.0.1'},
			{'name': 'Leaf1', 'description': '', 'version': '1.1.0'},
			{'name': 'Leaf2', 'description': '', 'version': '1.0.0'},
			{'name': 'Leaf2', 'description': '', 'version': '2.0.0'},
			{'name': 'Leaf2', 'description': '', 'version': '2.1.0'},
			{'name': 'Leaf2', 'description': '', 'version': '3.0.5'},

			# basic - single leaf dependency
			{'name': 'Simple1', 'description': '', 'version': '1.0.0', 'dependencies': [Dep('Leaf1', '[1.0]')]},
			# fixed dependency
			{'name': 'Simple1', 'description': '', 'version': '2.0.0', 'dependencies': [Dep('Leaf1', '1.1')]},
			# min dependency

			{'name': 'Simple2', 'description': '', 'version': '1.1.0', 'dependencies': [Dep('Leaf2', '[,2.0)')]},
			# any thing below 2
			{'name': 'Simple2', 'description': '', 'version': '2.0.5', 'dependencies': [Dep('Leaf2', '[2.0,3.0)')]},
			# only major version 2
		]

		for p in packages:
			p = Package.from_dict(p)
			versions = helper.packages_info_cache.setdefault(p.name, {})
			versions[p.version] = p

	@classmethod
	def tearDownClass(cls) -> None:
		helper.packages_info_cache.clear()
		helper.packages_info_cache.update(cls._original_cache)

	def test_find_single_package(self):
		cases = [
			('Leaf1', None, '1.1.0'),
			('Leaf2', None, '3.0.5'),
			('Leaf1', '(,1.1.0)', '1.0.1'),
			('Leaf1', '[1.0.0,1.1.0)', '1.0.1'),
			('Leaf1', '[1.0]', '1.0.1'),
			('Leaf2', '(2.0 , 3.0)', '2.1.0'),
			('Leaf2', '(, 3.0)', '2.1.0'),
			('Leaf2', '(, 3.0]', '3.0.5'),
			('Leaf2', '(, 2.5]', '2.1.0'),
		]

		for name, req, ver in cases:
			d = deps.find_dependencies([(name, req)])

			self.assertEqual(len(d.items()), 1)
			self.assertEqual(d[name].to_str(), ver)


	def test_find_no_match(self):
		# simple un-satisfied dependency
		cases = [
			('Leaf1', '[1.2,)'),
			('Leaf1', '[,1.0)'),
			('Leaf2', '(2.1,3.0)'),
			('Leaf2', '[4.0,2.0]'),
			('Leaf2', '[,0.0]'),
		]

		for name, req in cases:
			with self.assertRaises(Exception):
				deps.find_dependencies([(name, req)])

	def test_simple_multiple_matches(self):
		# cases with multiple dependencies
		cases = [
			('Simple1', '[1.0]', {'Simple1': Version.from_str('1.0.0'), 'Leaf1': Version.from_str('1.0.1')}),
			('Simple1', '[1.0]', {'Simple1': Version.from_str('1.0.0'), 'Leaf1': Version.from_str('1.0.1')}),
		]
		for (name, req, result) in cases:
			d = deps.find_dependencies([(name, req)])
			self.assertDictEqual(d, result)

if __name__ == '__main__':
	unittest.main()