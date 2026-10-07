
import unittest

from povshift.detector import POVShiftDetector


class Test_Focus_Tracker(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()
    
    def test_tc_10_initial_focus(self):
        clauses = self.detector.analyze("John wondered about Mary.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")

    def test_tc_11_same_focus_through_coreference(self):
        clauses = self.detector.analyze("John wondered about Mary. He felt nervous.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")
        self.assertEqual(focus[1].character.canonical_name, "John")

    def test_tc_12_focus_change(self):
        clauses = self.detector.analyze("John wondered about Mary. Mary knew he was waiting.")
        resolved = self.detector.resolve_coreference(clauses)
        enriched = self.detector.detect_internal_states(resolved)
        focus = self.detector.update_focus(enriched)

        self.assertEqual(focus[0].character.canonical_name, "John")
        self.assertEqual(focus[1].character.canonical_name, "Mary")
