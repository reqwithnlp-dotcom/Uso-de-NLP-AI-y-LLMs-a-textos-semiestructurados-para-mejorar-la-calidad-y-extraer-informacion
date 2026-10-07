
import unittest

from povshift.detector import POVShiftDetector


class Test_Parser(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()

    def test_tc_01_simple_clause(self):
        clauses = self.detector.analyze("John opened the door.")

        self.assertEqual(len(clauses), 1)
        self.assertEqual(clauses[0].text, "John opened the door.")
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertIsNotNone(clauses[0].subject)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[0].verb, "open")

    def test_tc_02_multiple_sentences(self):
        clauses = self.detector.analyze("John opened the door. Mary entered.")

        self.assertEqual(len(clauses), 2)
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertEqual(clauses[1].sentence_index, 1)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[1].subject.canonical_name, "Mary")
        self.assertEqual(clauses[0].verb, "open")
        self.assertEqual(clauses[1].verb, "enter")

    def test_tc_03_empty_text(self):
        with self.assertRaises(ValueError):
            self.detector.analyze("")
