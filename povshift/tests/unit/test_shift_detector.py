
import unittest

from povshift.detector import POVShiftDetector


class Test_Shift_Detector(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()
    
    def test_tc_13_clear_pov_shift(self):
        shifts = self.detector.detect("John wondered where Mary was. Mary knew he was waiting.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "John")
        self.assertEqual(shifts[0].to_character.canonical_name, "Mary")

    def test_tc_14_no_pov_shift_with_coreference(self):
        shifts = self.detector.detect("John wondered where Mary was. He knew she was coming.")

        self.assertEqual(shifts, [])

    def test_tc_15_character_change_without_pov_shift(self):
        shifts = self.detector.detect("John opened the door. Mary entered.")

        self.assertEqual(shifts, [])

    def test_tc_16_person_shift_without_internal_state(self):
        shifts = self.detector.detect("I opened the door. You closed it.")

        self.assertEqual(shifts, [])

    def test_tc_17_person_shift_with_internal_state(self):
        shifts = self.detector.detect("I felt nervous. You felt angry.")

        self.assertEqual(len(shifts), 1)
        self.assertEqual(shifts[0].from_character.canonical_name, "I")
        self.assertEqual(shifts[0].to_character.canonical_name, "You")


    def test_tc_22_multiple_clauses_same_sentence(self):
        clauses = self.detector.analyze("John opened the door and Mary felt afraid.")

        self.assertEqual(len(clauses), 2)
        self.assertEqual(clauses[0].sentence_index, 0)
        self.assertEqual(clauses[1].sentence_index, 0)
        self.assertEqual(clauses[0].subject.canonical_name, "John")
        self.assertEqual(clauses[1].subject.canonical_name, "Mary")
        self.assertFalse(clauses[0].internal_state)
        self.assertFalse(clauses[1].internal_state)
    
    
    def test_tc_24_confidence(self):
        shifts = self.detector.detect("John wondered where Mary was. Mary knew he was waiting.")

        self.assertEqual(len(shifts), 1)
        self.assertGreaterEqual(shifts[0].confidence, 0.0)
        self.assertLessEqual(shifts[0].confidence, 1.0)