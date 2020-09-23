import unittest
from models.taxonomy import Taxonomy, load_taxonomy

class TestTaxonomy(unittest.TestCase):

    def setUp(self):
        self.tax_1 = Taxonomy(name='bloom', num_of_verb_cats=6, verb_cat_names=['knowledge', 'comprehension', 'application', 'analysis', 'synthesis', 'evaluation'], filename_verbs_txt="./fixtures/test_V_B.txt")

    def tearDown(self):
        pass

    def test_len(self):
        self.tax_1.num_of_verb_cats = 0
        self.assertEqual(self.tax_1.__len__(), 6)

    def test_getitem(self):
        self.assertEqual(self.tax_1.__getitem__(3).name, 'ANALYSIS')

    def test_set_num_verb_cats(self):
        self.tax_1.set_num_verb_cats(4)
        self.assertEqual(self.tax_1.num_of_verb_cats, 4)
        self.assertRaises(TypeError, self.tax_1.set_num_verb_cats, 2.7)
        self.assertRaises(TypeError, self.tax_1.set_num_verb_cats, 'Fkhb')

    def test_set_num_verb_cats_from_file(self):
        self.tax_1.num_of_verb_cats = 0
        self.tax_1.set_num_verb_cats_from_file(self.tax_1.filename_verbs_txt)
        self.assertEqual(self.tax_1.num_of_verb_cats, 6)

    def test_add_verb_cat_name(self):
        self.assertEqual(self.tax_1.add_verb_cat_name("dummy"), True)
        self.assertEqual(len(self.tax_1.verb_cat_names), 7)
        self.assertEqual(self.tax_1.add_verb_cat_name("dummy"), False)
        self.assertEqual(len(self.tax_1.verb_cat_names), 7)

    def test_add_verb_cat_names(self):
        self.tax_1.add_verb_cat_names(["dummy_1", "dummy_2", "analysis"])
        self.assertEqual(len(self.tax_1.verb_cat_names), 8)

    def test_add_verb_cat(self):
        self.tax_1.add_verb_cat(cat_name="dummy")
        self.assertEqual(self.tax_1.num_of_verb_cats, 7)
        self.assertEqual(len(self.tax_1.verb_cats), 7)
        self.assertEqual(len(self.tax_1), 7)
        self.assertEqual(self.tax_1.add_verb_cat(cat_name="dummy"), False)

    def test_remove_verb_cat(self):
        self.tax_1.remove_verb_cat("dummy")
        self.assertEqual(len(self.tax_1.verb_cats), 6)
        self.assertEqual(len(self.tax_1), 6)
        self.assertEqual(self.tax_1.num_of_verb_cats, 6)
        self.tax_1.remove_verb_cat("knowledge")
        self.assertEqual(len(self.tax_1.verb_cats), 5)
        self.assertEqual(len(self.tax_1), 5)
        self.assertEqual(self.tax_1.num_of_verb_cats, 5)

    def test_remove_verb_cats(self):
        self.tax_1.remove_verb_cats()
        self.assertEqual(len(self.tax_1.verb_cats), 0)
        self.assertEqual(len(self.tax_1), 0)
        self.assertEqual(self.tax_1.num_of_verb_cats, 0)

    def test_initialise_verb_cats(self):
        self.tax_1.initialise_verb_cats()
        self.assertEqual(self.tax_1.num_of_verb_cats, 6)

if __name__ == '__main__':
    unittest.main()
