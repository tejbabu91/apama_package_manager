import unittest
from deps import VersionRange
from model import Version

class TestVersionRangeChecking(unittest.TestCase):
	def test_valid(self):
		cases = [
			('[1.0,2.0)', '1.0.0', True),
			('[1.0,2.0)', '1.0.1', True),
			('[1.0,2.0)', '1.9.0', True),
			('[1.0,2.0)', '1.9.9', True),
			('[1.0,2.0)', '2.0.0', False),
			('[1.0,2.0)', '2.0.1', False),
			('[1.0,2.0)', '0.9.9', False),
			('[1.0,2.0)', '9.9.9', False),
			('[1.0,)', '1.0.1', True),
			('[1.0,)', '11.0.1', True),
			('[1.0,)', '0.9.9', False),
		]

		for (r, v, inRange) in cases:
			_range = VersionRange.from_str(r)
			ver = Version.from_str(v)
			self.assertEqual(inRange, _range.isInRange(ver))


if __name__ == '__main__':
	unittest.main()