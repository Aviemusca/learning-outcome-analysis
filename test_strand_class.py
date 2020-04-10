import unittest
from strand_class import Strand

class TestStrand(unittest.TestCase):

    def setUp(self):
        self.strand_1 = Strand("core concepts")
    def tearDown(self):
        pass

    def test_load_LOs_from_file(self):
        self.strand_1.load_LOs_from_file("test_LO_CS.txt", 0)
        self.assertEqual(len(self.strand_1.LOs), 23)

    def test_load_LOs_from_file_2(self):
        self.strand_1.load_LOs_from_file("test_LO_CS.txt", 1)
        self.assertEqual(len(self.strand_1.LOs), 22)

if __name__ == '__main__':
    unittest.main()
