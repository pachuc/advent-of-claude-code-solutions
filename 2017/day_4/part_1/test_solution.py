import unittest
from solution import is_valid_passphrase


class TestPassphraseValidation(unittest.TestCase):

    def test_example_valid(self):
        """Test from problem: all unique words"""
        self.assertTrue(is_valid_passphrase("aa bb cc dd ee"))

    def test_example_invalid(self):
        """Test from problem: duplicate word"""
        self.assertFalse(is_valid_passphrase("aa bb cc dd aa"))

    def test_example_similar_words(self):
        """Test from problem: similar but different words"""
        self.assertTrue(is_valid_passphrase("aa bb cc dd aaa"))

    def test_single_word(self):
        """Edge case: single word"""
        self.assertTrue(is_valid_passphrase("word"))

    def test_two_identical(self):
        """Edge case: two identical words"""
        self.assertFalse(is_valid_passphrase("word word"))

    def test_two_different(self):
        """Edge case: two different words"""
        self.assertTrue(is_valid_passphrase("word1 word2"))

    def test_empty(self):
        """Edge case: empty passphrase"""
        self.assertTrue(is_valid_passphrase(""))

    def test_multiple_spaces(self):
        """Edge case: multiple spaces between words"""
        self.assertTrue(is_valid_passphrase("aa  bb   cc"))

    def test_whitespace(self):
        """Edge case: leading/trailing whitespace"""
        self.assertTrue(is_valid_passphrase("  aa bb cc  "))

    def test_triple_duplicate(self):
        """Edge case: word appears three times"""
        self.assertFalse(is_valid_passphrase("aa aa aa"))

    def test_duplicate_at_ends(self):
        """Edge case: duplicate at start and end"""
        self.assertFalse(is_valid_passphrase("aa bb cc aa"))

    def test_input_line_20(self):
        """Real input: line 20 has duplicate 'duciqf'"""
        self.assertFalse(is_valid_passphrase("hmo fdayx duciqf cgt duciqf"))

    def test_input_line_54(self):
        """Real input: line 54 has duplicate 'rrol'"""
        self.assertFalse(is_valid_passphrase("oicgs rrol zvnbna rrol"))

    def test_input_line_1(self):
        """Real input: line 1 is valid"""
        self.assertTrue(is_valid_passphrase("bdwdjjo avricm cjbmj ran lmfsom ivsof"))


if __name__ == '__main__':
    unittest.main()
