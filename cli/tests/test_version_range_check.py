import unittest
from deps import VersionRange

class TestVersionRangeParsing(unittest.TestCase):
	def test_valid(self):
		for s, r in [
		    ('1.0', '[1.0,)'),

		    ('[1.0]', '[1.0,1.0]'),

		    ('[1.0,]', '[1.0,)'),
		    ('[1.0,)', '[1.0,)'),
		    ('[,1.0]', '(,1.0]'),
		    ('[,1.0)', '(,1.0)'),

		    ('(1.0,)', '(1.0,)'),
		    ('(1.0,]', '(1.0,)'),
		    ('(,1.0)', '(,1.0)'),
		    ('(,1.0]', '(,1.0]'),

		    ('[1.0,2.0]', '[1.0,2.0]'),
		    ('(1.0,2.0)', '(1.0,2.0)'),
		    ('(1.0,2.0]', '(1.0,2.0]'),
		    ('[1.0,2.0)', '[1.0,2.0)'),
	    ]:
			v = VersionRange.from_str(s)
		self.assertEqual(str(v), r)

	def test_invalid(self):
		for s, r in [
		    ('(1.0)', None),
		    ('(1.0', None),
		    ('[1.0)', None),
		    ('[1.0,2.3,4.5]', None),
		    ('[5.0,4.0]', None),  # will never be satisfied
		    ('(5.0,5.0]', None),  # will never be satisfied
		    ('[5.0,5.0)', None),
		    ('(5.0,5.0)', None),
	    ]:
			with self.assertRaises(Exception):
				_ = VersionRange.from_str(s)

if __name__ == '__main__':
	unittest.main()