import unittest

from pyard.smart_sort import smart_sort_comparator


class TestSmartSort(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_same_comparator(self):
        allele = "HLA-A*01:01"
        self.assertEqual(smart_sort_comparator(allele, allele), 0)

    def test_equal_comparator(self):
        allele1 = "HLA-A*01:01"
        allele2 = "HLA-A*01:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 0)

    def test_equal_comparator_G(self):
        # Should compare without G
        allele1 = "HLA-A*01:01G"
        allele2 = "HLA-A*01:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 0)

    def test_equal_comparator_NG(self):
        # Should compare without N and G
        allele1 = "HLA-A*01:01G"
        allele2 = "HLA-A*01:01N"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 0)

    def test_first_field_comparator_le(self):
        allele1 = "HLA-A*01:01"
        allele2 = "HLA-A*02:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_first_field_comparator_ge(self):
        allele1 = "HLA-A*02:01"
        allele2 = "HLA-A*01:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 1)

    def test_second_field_comparator_le(self):
        allele1 = "HLA-A*01:01"
        allele2 = "HLA-A*01:02"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_second_field_comparator_le_smart(self):
        allele1 = "HLA-A*01:29"
        allele2 = "HLA-A*01:100"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_second_field_comparator_ge(self):
        allele1 = "HLA-A*01:02"
        allele2 = "HLA-A*01:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 1)

    def test_third_field_comparator_le(self):
        allele1 = "HLA-A*01:01:01"
        allele2 = "HLA-A*01:01:20"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_third_field_comparator_le_smart(self):
        allele1 = "HLA-A*01:01:29"
        allele2 = "HLA-A*01:01:100"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_third_field_comparator_ge(self):
        allele1 = "HLA-A*01:01:02"
        allele2 = "HLA-A*01:01:01"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 1)

    def test_fourth_field_comparator_le(self):
        allele1 = "HLA-A*01:01:01:01"
        allele2 = "HLA-A*01:01:01:20"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_fourth_field_comparator_le_smart(self):
        allele1 = "HLA-A*01:01:01:39"
        allele2 = "HLA-A*01:01:01:200"
        self.assertEqual(smart_sort_comparator(allele1, allele2), -1)

    def test_fourth_field_comparator_ge(self):
        allele1 = "HLA-A*01:01:01:30"
        allele2 = "HLA-A*01:01:01:09"
        self.assertEqual(smart_sort_comparator(allele1, allele2), 1)


if __name__ == '__main__':
    unittest.main()
