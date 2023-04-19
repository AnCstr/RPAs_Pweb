import unittest
from utils.split_excel import Spliter


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.spliter = Spliter()

    def test_something(self):
        self.assertIsInstance(self.spliter, Spliter)


if __name__ == '__main__':
    unittest.main()
