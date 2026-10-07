
import unittest

from povshift.detector import POVShiftDetector


class Test_Pov_Detector(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()
    
    def test_tc_18_complete_pipeline_shift(self):
        shifts = self.detector.detect("John wondered where Mary was. Mary knew he was waiting.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "John")
        self.assertEqual(shifts[0].to_character.canonical_name, "Mary")

    def test_tc_19_complete_pipeline_no_shift(self):
        shifts = self.detector.detect("John wondered where Mary was. He felt nervous. He remembered their conversation.")

        self.assertEqual(shifts, [])

    def test_tc_20_multiple_shifts(self):
        shifts = self.detector.detect("John wondered where Mary was. Mary knew he was waiting. John remembered the conversation.")

        self.assertEqual(len(shifts), 2)
        self.assertEqual(shifts[0].from_character.canonical_name, "John")
        self.assertEqual(shifts[0].to_character.canonical_name, "Mary")
        self.assertEqual(shifts[1].from_character.canonical_name, "Mary")
    
        self.assertEqual(shifts[1].to_character.canonical_name, "John")

    def test_tc_21_coreference_prevents_false_shift(self):
        shifts = self.detector.detect("John wondered where Mary was. He felt nervous. Mary knew he was waiting.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "John")
        self.assertEqual(shifts[0].to_character.canonical_name, "Mary")


