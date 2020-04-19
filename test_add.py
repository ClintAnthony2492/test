import unittest
import add

class TestSuite(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add.add(1,2), 3)

if __name__ == '__main__':
    unittest.main()