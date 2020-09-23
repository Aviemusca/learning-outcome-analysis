import unittest
from models.curriculum import Curriculum, LO_list_to_dict, dict_to_LO_list

class TestCurriculum(unittest.TestCase):
    def setUp(self):
        self.curr_1 = Curriculum(name="computer_science", country="ireland", ID="n/a", num_of_strands=3, strand_names=["core concepts", "practices and principles", "applied learning tasks"], filename_LOs_txt="./fixtures/test_LO_CS.txt")

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.curr_1.name, "COMPUTER_SCIENCE")
        self.assertEqual(self.curr_1.country, "Ireland")
        self.assertEqual(self.curr_1.ID, "n/a")
        self.assertEqual(self.curr_1.num_of_strands, 3)
        self.assertEqual(self.curr_1.strand_names[0], "CORE CONCEPTS")


    def test_set_num_of_strands(self):
        self.assertRaises(TypeError, self.curr_1.set_num_of_strands, 2.5)
        self.assertRaises(TypeError, self.curr_1.set_num_of_strands, "igs")

    def test_set_num_strands_from_file(self):
        self.curr_1.set_num_of_strands(0)
        self.curr_1.set_num_strands_from_file(self.curr_1.filename_LOs_txt)
        self.assertEqual(self.curr_1.num_of_strands, 3)

    def test_add_strand_name(self):
        self.curr_1.add_strand_name("dummy")
        self.assertEqual(len(self.curr_1.strand_names), 4)
        self.assertEqual(self.curr_1.add_strand_name("dummy"), False)
        self.assertEqual(len(self.curr_1.strand_names), 4)

    def test_add_strand_names(self):
        self.curr_1.add_strand_names(["dummy", "dummy_2"])
        self.assertEqual(len(self.curr_1.strand_names), 5)
        self.curr_1.add_strand_names(["dummy", "dummy_2"])
        self.assertEqual(len(self.curr_1.strand_names), 5)

    def test_load_LOs_from_file(self):
        self.curr_1.load_LOs_from_file(self.curr_1.filename_LOs_txt)
        self.assertEqual([len(self.curr_1.LOs[i]) for i in range(3)], [23, 22, 14])
        self.assertEqual(self.curr_1.LOs[1][-1].text, "students can explain the different stages in software testing")
        self.assertEqual(self.curr_1.LOs[2][-2].text, "students can develop a program that utilises digital and analogue inputs")

    def test_list_to_dict_conversion(self):
        """ This simulataneously tests LO_list_to_dict and dict_to_LO_list (inverse functions) """
        self.curr_1.load_LOs_from_file(self.curr_1.filename_LOs_txt)
        LO_dict = LO_list_to_dict(self.curr_1.LOs, self.curr_1.strand_names)
        LO_list = dict_to_LO_list(LO_dict)
        LO_dict_2 = LO_list_to_dict(LO_list, self.curr_1.strand_names)
        self.assertEqual(LO_dict, LO_dict_2)


    def test_getitem(self):
        self.curr_1.load_LOs_from_file(self.curr_1.filename_LOs_txt)
        dict_1, i = {}, 0
        for strand in self.curr_1.LOs:
            for LO in strand:
                dict_1[i] = LO.text
                i += 1
        dict_2 = {i : LO.text for i, LO in enumerate(self.curr_1)}
        self.assertEqual(dict_1, dict_2)

if __name__ == '__main__':
    unittest.main()

