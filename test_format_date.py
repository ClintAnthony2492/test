import unittest
import post_process_logs as pp_logs

class TestSuite(unittest.TestCase):
    def test_format_date(self):
        self.assertEqual(pp_logs.format_date(20592), "May 02, 1992")
        self.assertEqual(pp_logs.format_date(221192), "November 22, 1992")
        self.assertEqual(pp_logs.format_date(240820), "August 24, 2020")

if __name__ == '__main__':
    unittest.main()