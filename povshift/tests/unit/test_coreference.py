
import unittest

from povshift.detector import POVShiftDetector


class Test_Coreference(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()
    
    def test_tc_04_coreference(self):
        clauses = self.detector.analyze("John entered the room. He sat down.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertEqual(resolved[1].subject.canonical_name, "John")
        self.assertEqual(resolved[1].subject.mentions, ["John", "He"])

    def test_tc_05_female_coreference(self):
        clauses = self.detector.analyze("Mary entered the room. She sat down.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertEqual(resolved[1].subject.canonical_name, "Mary")
        self.assertEqual(resolved[1].subject.mentions, ["Mary", "She"])

    def test_tc_06_ambiguous_coreference(self):
        clauses = self.detector.analyze("John met Paul. He smiled.")
        resolved = self.detector.resolve_coreference(clauses)

        self.assertIsNone(resolved[1].subject)
