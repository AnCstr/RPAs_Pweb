import unittest
from utils.split_excel import Diretorio


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.diretorio = Diretorio()

    def test_something(self):
        self.assertIsInstance(self.diretorio, Diretorio)


if __name__ == '__main__':
    unittest.main()
