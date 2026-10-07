
import unittest

from povshift.detector import POVShiftDetector


class Test_Internal_States(unittest.TestCase):
    def setUp(self):
        self.detector = POVShiftDetector()
    
    
    def test_tc_07_cognitive_state(self):
        clauses = self.detector.analyze("John wondered where Mary was.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertTrue(enriched[0].internal_state)
        self.assertEqual(enriched[0].state_type, "cognition")
        self.assertEqual(enriched[0].experiencer.canonical_name, "John")
    
    
    def test_tc_08_emotional_state(self):
        clauses = self.detector.analyze("Mary felt afraid.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertTrue(enriched[0].internal_state)
        self.assertEqual(enriched[0].state_type, "emotion")
        self.assertEqual(enriched[0].experiencer.canonical_name, "Mary")


    def test_tc_09_observable_action(self):
        clauses = self.detector.analyze("John opened the door.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertFalse(enriched[0].internal_state)
        self.assertIsNone(enriched[0].state_type)
        self.assertIsNone(enriched[0].experiencer)

    def test_tc_23_perception_state(self):
        clauses = self.detector.analyze("John saw Mary leaving the room.")
        enriched = self.detector.detect_internal_states(clauses)

        self.assertTrue(enriched[0].internal_state)
        self.assertEqual(enriched[0].state_type, "perception")
        self.assertEqual(enriched[0].experiencer.canonical_name, "John")